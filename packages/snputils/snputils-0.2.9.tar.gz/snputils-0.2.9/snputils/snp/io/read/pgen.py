import logging
import os
from typing import List, Optional

import numpy as np
import polars as pl
import pgenlib as pg

from snputils.snp.genobj.snpobj import SNPObject
from snputils.snp.io.read.base import SNPBaseReader

log = logging.getLogger(__name__)


@SNPBaseReader.register
class PGENReader(SNPBaseReader):
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
        Read a pgen fileset (pgen, psam, pvar) into a SNPObject.

        Args:
            fields (str, None, or list of str, optional): Fields to extract data for that should be included in the returned SNPObject.
                Available fields are 'GT', 'IID', 'REF', 'ALT', '#CHROM', 'ID', 'POS', 'FILTER', 'QUAL'.
                To extract all fields, set fields to None. Defaults to None.
            exclude_fields (str, None, or list of str, optional): Fields to exclude from the returned SNPObject.
                Available fields are 'GT', 'IID', 'REF', 'ALT', '#CHROM', 'ID', 'POS', 'FILTER', 'QUAL'.
                To exclude no fields, set exclude_fields to None. Defaults to None.
            sample_ids: List of sample IDs to read. If None and sample_idxs is None, all samples are read.
            sample_idxs: List of sample indices to read. If None and sample_ids is None, all samples are read.
            variant_ids: List of variant IDs to read. If None and variant_idxs is None, all variants are read.
            variant_idxs: List of variant indices to read. If None and variant_ids is None, all variants are read.
            phased: Whether to read and store the genotypes as phased.
                Note that due to the pgenlib backend, when phased is True, 8 times as much RAM is required.
                Nonetheless, the calldata_gt will only be double the size.

        Returns:
            snpobj: SNPObject containing the data from the pgen fileset.
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

        fields = fields or ["GT", "IID", "REF", "ALT", "#CHROM", "ID", "POS", "FILTER", "QUAL"]
        exclude_fields = exclude_fields or []
        fields = [field for field in fields if field not in exclude_fields]
        only_read_pgen = fields == ["GT"] and variant_idxs is None and sample_idxs is None

        filename_noext = str(self.filename)
        for ext in [".pgen", ".pvar", ".pvar.zst", ".psam"]:
            if filename_noext.endswith(ext):
                filename_noext = filename_noext[:-len(ext)]
                break

        if only_read_pgen:
            file_num_samples = None  # Not needed for pgen
            file_num_variants = None  # Not needed
        else:
            pvar_extensions = [".pvar", ".pvar.zst"]
            pvar_filename = None
            for ext in pvar_extensions:
                possible_pvar = filename_noext + ext
                if os.path.exists(possible_pvar):
                    pvar_filename = possible_pvar
                    break
            if pvar_filename is None:
                raise FileNotFoundError(f"No .pvar or .pvar.zst file found for {filename_noext}")

            log.info(f"Reading {pvar_filename}")

            def open_textfile(filename):
                if filename.endswith('.zst'):
                    import zstandard as zstd
                    return zstd.open(filename, 'rt')
                else:
                    return open(filename, 'rt')

            pvar_has_header = True
            pvar_header_line_num = 0
            with open_textfile(pvar_filename) as file:
                for line_num, line in enumerate(file):
                    if line.startswith("#CHROM"):
                        pvar_header_line_num = line_num
                        break
                else:  # if no break
                    pvar_has_header = False

            pvar = pl.scan_csv(
                pvar_filename,
                separator='\t',
                skip_rows=pvar_header_line_num,
                has_header=pvar_has_header,
                new_columns=None if pvar_has_header else ["#CHROM", "ID", "CM", "POS", "REF", "ALT"],
                schema_overrides={
                    "#CHROM": pl.String,
                    "POS": pl.Int64,
                    "ID": pl.String,
                    "REF": pl.String,
                    "ALT": pl.String,
                },
            ).with_row_index()

            # since pvar is lazy, the skip_rows operation hasn't materialized
            # pl.len() will return the length of the pvar + header
            file_num_variants = pvar.select(pl.len()).collect().item() - pvar_header_line_num

            if variant_ids is not None:
                variant_idxs = (
                    pvar.filter(pl.col("ID").is_in(variant_ids))
                    .select("index")
                    .collect()
                    .to_series()
                    .to_numpy()
                )

            if variant_idxs is None:
                num_variants = file_num_variants
                variant_idxs = np.arange(num_variants, dtype=np.uint32)
                pvar = pvar.collect()
            else:
                num_variants = np.size(variant_idxs)
                variant_idxs = np.array(variant_idxs, dtype=np.uint32)
                pvar = pvar.filter(pl.col("index").is_in(variant_idxs)).collect()

            log.info(f"Reading {filename_noext}.psam")

            with open(filename_noext + ".psam") as file:
                first_line = file.readline().strip()
                psam_has_header = first_line.startswith(("#FID", "FID", "#IID", "IID"))

            psam = pl.read_csv(
                filename_noext + ".psam",
                separator='\t',
                has_header=psam_has_header,
                new_columns=None if psam_has_header else ["FID", "IID", "PAT", "MAT", "SEX", "PHENO1"],
            ).with_row_index()
            if "#IID" in psam.columns:
                psam = psam.rename({"#IID": "IID"})
            if "#FID" in psam.columns:
                psam = psam.rename({"#FID": "FID"})

            file_num_samples = psam.height

            if sample_ids is not None:
                sample_idxs = (
                    psam.filter(pl.col("IID").is_in(sample_ids))
                    .select("index")
                    .to_series()
                    .to_numpy()
                )

            if sample_idxs is None:
                num_samples = file_num_samples
            else:
                num_samples = np.size(sample_idxs)
                sample_idxs = np.array(sample_idxs, dtype=np.uint32)
                psam = psam.filter(pl.col("index").is_in(sample_idxs))

        if "GT" in fields:
            log.info(f"Reading {filename_noext}.pgen")
            pgen_reader = pg.PgenReader(
                str.encode(filename_noext + ".pgen"),
                raw_sample_ct=file_num_samples,
                variant_ct=file_num_variants,
                sample_subset=sample_idxs,
            )

            if only_read_pgen:
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
            samples=psam.get_column("IID").to_numpy() if "IID" in psam.columns and fields else None,
            variants_ref=pvar.get_column("REF").to_numpy() if "REF" in pvar.columns and fields else None,
            variants_alt=pvar.get_column("ALT").to_numpy() if "ALT" in pvar.columns and fields else None,
            variants_chrom=pvar.get_column("#CHROM").to_numpy() if "#CHROM" in pvar.columns and fields else None,
            variants_id=pvar.get_column("ID").to_numpy() if "ID" in pvar.columns and fields else None,
            variants_pos=pvar.get_column("POS").to_numpy() if "POS" in pvar.columns and fields else None,
            variants_filter_pass=pvar.get_column("FILTER").to_numpy() if "FILTER" in pvar.columns and fields else None,
            variants_qual=pvar.get_column("QUAL").to_numpy() if "QUAL" in pvar.columns and fields else None,
        )

        log.info("Finished constructing SNPObject")
        return snpobj
