import logging
from typing import List, Optional

import numpy as np
import polars as pl
import pgenlib as pg

from snputils.snp.genobj.snpobj import SNPObject
from snputils.snp.io.read.base import SNPBaseReader

log = logging.getLogger(__name__)


@SNPBaseReader.register
class BEDReader(SNPBaseReader):
    def read(
        self,
        fields: Optional[List[str]] = None,
        exclude_fields: Optional[List[str]] = None,
        sample_ids: Optional[np.ndarray] = None,
        sample_idxs: Optional[np.ndarray] = None,
        variant_ids: Optional[np.ndarray] = None,
        variant_idxs: Optional[np.ndarray] = None,
        phased: bool = False,
        n_jobs: int = 1
    ) -> SNPObject:
        """
        Read a bed fileset (bed, bim, fam) into a SNPObject.

        Args:
            fields (str, None, or list of str, optional): Fields to extract data for that should be included in the returned SNPObject.
                Available fields are 'GT', 'IID', 'REF', 'ALT', '#CHROM', 'ID', 'POS'.
                To extract all fields, set fields to None. Defaults to None.
            exclude_fields (str, None, or list of str, optional): Fields to exclude from the returned SNPObject.
                Available fields are 'GT', 'IID', 'REF', 'ALT', '#CHROM', 'ID', 'POS'.
                To exclude no fields, set exclude_fields to None. Defaults to None.
            sample_ids: List of sample IDs to read. If None and sample_idxs is None, all samples are read.
            sample_idxs: List of sample indices to read. If None and sample_ids is None, all samples are read.
            variant_ids: List of variant IDs to read. If None and variant_idxs is None, all variants are read.
            variant_idxs: List of variant indices to read. If None and variant_ids is None, all variants are read.
            phased: Whether to read and store the genotypes as phased.
                Note that due to the pgenlib backend, when phased is True, 8 times as much RAM is required.
                Nonetheless, the calldata_gt will only be double the size.
                WARNING: bed files do not store phase information. If you need it, use vcf or pgen.

        Returns:
            snpobj: SNPObject containing the data from the bed fileset.
                If phased is True, calldata_gt is stored as a numpy array of shape (num_variants, num_samples, 2) and dtype int8 containing 0, 1.
                If phased is False, calldata_gt is stored as a numpy array of shape (num_variants, num_samples) and dtype int8 containing 0, 1, 2.

        Raises:
            AssertionError: If both sample_idxs and sample_ids are specified.
            AssertionError: If both variant_idxs and variant_ids are specified.
        """
        assert (
            sample_idxs is None or sample_ids is None
        ), "Only one of sample_idxs and sample_ids can be specified"
        assert (
            variant_idxs is None or variant_ids is None
        ), "Only one of variant_idxs and variant_ids can be specified"

        if isinstance(fields, str):
            fields = [fields]
        if isinstance(exclude_fields, str):
            exclude_fields = [exclude_fields]

        fields = fields or ["GT", "IID", "REF", "ALT", "#CHROM", "ID", "POS"]
        exclude_fields = exclude_fields or []
        fields = [field for field in fields if field not in exclude_fields]
        only_read_bed = fields == ["GT"] and variant_idxs is None and sample_idxs is None

        filename_noext = str(self.filename)
        if filename_noext[-4:].lower() in (".bed", ".bim", ".fam"):
            filename_noext = filename_noext[:-4]

        if only_read_bed:
            with open(filename_noext + '.fam', 'r') as f:
                file_num_samples = sum(1 for _ in f)  # Get sample count from fam file
            file_num_variants = None  # Not needed
        else:
            log.info(f"Reading {filename_noext}.bim")

            bim = pl.read_csv(
                filename_noext + ".bim",
                separator='\t',
                has_header=False,
                new_columns=["#CHROM", "ID", "CM", "POS", "ALT", "REF"],
                schema_overrides={
                    "#CHROM": pl.String,
                    "ID": pl.String,
                    "CM": pl.Float64,
                    "POS": pl.Int64,
                    "ALT": pl.String,
                    "REF": pl.String
                }
            )
            file_num_variants = bim.height

            if variant_ids is not None:
                variant_idxs = bim.filter(pl.col("ID").is_in(variant_ids)).row_nr().to_numpy()

            if variant_idxs is None:
                num_variants = file_num_variants
                variant_idxs = np.arange(num_variants, dtype=np.uint32)
            else:
                num_variants = np.size(variant_idxs)
                variant_idxs = np.array(variant_idxs, dtype=np.uint32)
                bim = bim.filter(pl.col("row_nr").is_in(variant_idxs))

            log.info(f"Reading {filename_noext}.fam")

            fam = pl.read_csv(
                filename_noext + ".fam",
                separator='\t',
                has_header=False,
                new_columns=["Family ID", "IID", "Father ID",
                             "Mother ID", "Sex code", "Phenotype value"],
                schema_overrides={
                    "Family ID": pl.String,
                    "IID": pl.String,
                    "Father ID": pl.String,
                    "Mother ID": pl.String,
                    "Sex code": pl.Int64,
                    "Phenotype value": pl.Float64
                }
            )
            file_num_samples = fam.height

            if sample_ids is not None:
                sample_idxs = fam.filter(pl.col("IID").is_in(sample_ids)).row_nr().to_numpy()

            if sample_idxs is None:
                num_samples = file_num_samples
            else:
                num_samples = np.size(sample_idxs)
                sample_idxs = np.array(sample_idxs, dtype=np.uint32)
                fam = fam.filter(pl.col("row_nr").is_in(sample_idxs))

        if "GT" in fields:
            log.info(f"Reading {filename_noext}.bed")
            pgen_reader = pg.PgenReader(
                str.encode(filename_noext + ".bed"),
                raw_sample_ct=file_num_samples,
                variant_ct=file_num_variants,
                sample_subset=sample_idxs,
            )

            if only_read_bed:
                num_samples = pgen_reader.get_raw_sample_ct()
                num_variants = pgen_reader.get_variant_ct()
                variant_idxs = np.arange(num_variants, dtype=np.uint32)

            # required arrays: variant_idxs + sample_idxs + genotypes
            if phased:
                required_ram = (num_samples + num_variants + num_variants * 2 * num_samples) * 4
            else:
                required_ram = (num_samples + num_variants) * 4 + num_variants * num_samples
            log.info(f">{required_ram / 1024**3:.2f} GiB of RAM are required to process {num_samples} samples with {num_variants} variants each")

            if phased:
                genotypes = np.empty((num_variants, 2 * num_samples), dtype=np.int32)  # cannot use int8 because of pgenlib
                pgen_reader.read_alleles_list(variant_idxs, genotypes)
                genotypes = genotypes.astype(np.int8).reshape((num_variants, num_samples, 2))
            else:
                genotypes = np.empty((num_variants, num_samples), dtype=np.int8)
                pgen_reader.read_list(variant_idxs, genotypes)
            pgen_reader.close()
        else:
            genotypes = None

        log.info("Constructing SNPObject")

        snpobj = SNPObject(
            calldata_gt=genotypes if "GT" in fields else None,
            samples=fam.get_column("IID").to_numpy() if "IID" in fields else None,
            variants_ref=bim.get_column("REF").to_numpy() if "REF" in fields else None,
            variants_alt=bim.get_column("ALT").to_numpy() if "ALT" in fields else None,
            variants_chrom=bim.get_column("#CHROM").to_numpy() if "#CHROM" in fields else None,
            variants_id=bim.get_column("ID").to_numpy() if "ID" in fields else None,
            variants_pos=bim.get_column("POS").to_numpy() if "POS" in fields else None,
        )

        log.info("Finished constructing SNPObject")
        return snpobj
