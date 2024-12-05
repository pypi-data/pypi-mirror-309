import logging
from typing import Optional, List
from pathlib import Path
import gzip
import allel
import numpy as np
import polars as pl

from snputils.snp.genobj.snpobj import SNPObject
from snputils.snp.io.read.base import SNPBaseReader

log = logging.getLogger(__name__)


@SNPBaseReader.register
class VCFReader(SNPBaseReader):
    def read(
        self,
        fields: Optional[List[str]] = None,
        exclude_fields: Optional[List[str]] = None,
        rename_fields: Optional[dict] = None,
        fills: Optional[dict] = None,
        region: Optional[str] = None,
        samples: Optional[List[str]] = None,
        phased: bool = False,
    ) -> SNPObject:
        """
        Read a vcf file into a SNPObject.

        Args:
            fields: Fields to extract data for. e.g., ['variants/CHROM', 'variants/POS',
                'calldata/GT']. If you are feeling lazy, you can drop the 'variants/'
                and 'calldata/' prefixes, in which case the fields will be matched
                against fields declared in the VCF header, with variants taking priority
                over calldata if a field with the same ID exists both in INFO and FORMAT
                headers. I.e., ['CHROM', 'POS', 'DP', 'GT'] will work, although watch out
                for fields like 'DP' which can be both INFO and FORMAT. To extract all
                fields, provide just the string '*'. To extract all variants fields
                (including all INFO fields) provide 'variants/*'. To extract all
                calldata fields (i.e., defined in FORMAT headers) provide 'calldata/*'.
            exclude_fields: Fields to exclude. E.g., for use in combination with fields='*'.
            rename_fields: Fields to be renamed. Should be a dictionary mapping old to new names.
            fills: Override the fill value used for empty values. Should be a dictionary
                mapping field names to fill values.
            region: Genomic region to extract variants for. If provided, should be a
                tabix-style region string, which can be either just a chromosome name
                (e.g., '2L'), or a chromosome name followed by 1-based beginning and
                end coordinates (e.g., '2L:100000-200000'). Note that only variants
                whose start position (POS) is within the requested range will be included.
                This is slightly different from the default tabix behaviour, where a
                variant (e.g., deletion) may be included if its position (POS) occurs
                before the requested region but its reference allele overlaps the
                region - such a variant will not be included in the data returned
                by this function.
            samples: Selection of samples to extract calldata for. If provided, should be
                a list of strings giving sample identifiers. May also be a list of
                integers giving indices of selected samples.
            phased: Whether to store the genotypes as phased.

        Returns:
            snpobj: SNPObject containing the data from the vcf file.
                If phased is True, calldata_gt is stored as a numpy array of shape
                (num_variants, num_samples, 2) and dtype int8 containing 0, 1.
                If phased is False, calldata_gt is stored as a numpy array of shape
                (num_variants, num_samples) and dtype int8 containing 0, 1, 2.
        """
        log.info(f"Reading {self.filename}")

        vcf_dict = allel.read_vcf(
            str(self.filename),
            fields=fields,
            exclude_fields=exclude_fields,
            rename_fields=rename_fields,
            fills=fills,
            region=region,
            samples=samples,
        )
        assert vcf_dict is not None  # suppress Flake8 warning

        genotypes = vcf_dict["calldata/GT"].astype(np.int8)
        if not phased:
            genotypes = genotypes.sum(axis=2, dtype=np.int8)

        snpobj = SNPObject(
            calldata_gt=genotypes,
            samples=vcf_dict["samples"],
            variants_ref=vcf_dict["variants/REF"],
            variants_alt=vcf_dict["variants/ALT"],
            variants_chrom=vcf_dict["variants/CHROM"],
            variants_filter_pass=vcf_dict["variants/FILTER_PASS"],
            variants_id=vcf_dict["variants/ID"],
            variants_pos=vcf_dict["variants/POS"],
            variants_qual=vcf_dict["variants/QUAL"],
        )

        log.info(f"Finished reading {self.filename}")
        return snpobj


def _get_vcf_names(vcf_path: str):
    """
    Get the column names from a VCF file.

    Parameters
    ----------
    vcf_path: str or Path
        The path to the VCF file.

    Returns
    -------
    List[str]
        List of column names.
    """
    vcf_path = Path(vcf_path)
    if vcf_path.suffixes[-2:] == ['.vcf', '.gz']:
        open_func = gzip.open
        mode = 'rt'
    elif vcf_path.suffix == '.vcf':
        open_func = open
        mode = 'r'
    else:
        raise ValueError(f"Unsupported file extension: {vcf_path.suffixes}")

    with open_func(vcf_path, mode) as ifile:
        for line in ifile:
            if line.startswith("#CHROM"):
                vcf_names = [x.strip() for x in line.split('\t')]
                break

    return vcf_names


def _infer_data_types(names: List):
    """
    Infer data types for VCF columns.

    Parameters
    ----------
    names: List
        List of column names.

    Returns
    -------
    dict
        Dictionary mapping column names to data types.
    """
    dtype_options = {name: pl.Utf8 for name in names}
    dtype_options['POS'] = pl.Int32
    dtype_options['#CHROM'] = pl.String

    return dtype_options


def _extract_columns(names: List[str], fields: List[str], exclude_fields: List[str],
                     samples: List[str]) -> List[str]:
    """
    Extracts columns based on specified `fields`, `exclude_fields` and `samples`.

    Parameters
    ----------
    names: List
        List of column names.
    fields: list of strings, default=None
        Fields to extract data for. This parameter specifies which data fields
        from the VCF file should be included in the result. To extract all 
        fields, provide just the string '*'. 
    exclude_fields: list of strings, default=None
        Fields to exclude. E.g., for use in combination with fields='*'.
    samples: list of strings, default=None
        Selection of samples to extract calldata for. If provided, should be 
        a list of strings giving sample identifiers. May also be a list of 
        integers giving indices of selected samples.
    """
    # Define standard field names in a VCF file
    field_names = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']

    # Find the index of the first column that is not a standard field name
    first_sample_idx = next(i for i, col in enumerate(names) if col not in field_names)

    # Identify field columns as all columns before the first sample column
    field_columns = names[:first_sample_idx]

    if fields != '*' and fields is not None:
        # Filter field columns to contain those in `fields`
        field_columns = list(set(field_columns).intersection(set(fields)))
    elif fields == '*' and exclude_fields is not None:
        field_columns = list(set(field_columns) - set(exclude_fields))

    # Sample columns are all columns starting from the first sample column
    sample_columns = names[first_sample_idx:]

    if samples is not None:
        if len(samples) == 0:
            sample_columns = []
        elif type(samples[0]) is int:
            sample_columns = list(np.array(sample_columns)[samples])
        else:
            sample_columns = list(set(sample_columns).intersection(set(samples)))

    # Create a dictionary mapping column names to their indices
    column_idx_map = {name: index for index, name in enumerate(names)}

    # Create a list of selected column indices
    selected_column_idxs = [column_idx_map[col] for col in field_columns + sample_columns]

    # Sort the selected column indices
    selected_column_idxs.sort()

    return field_columns, sample_columns, selected_column_idxs


@SNPBaseReader.register
class VCFReaderPolars(SNPBaseReader):
    """Reads a VCF file and processes it into a SNPObject."""

    def __init__(self, filename: str):
        self._filename = filename

    def read(self,
             fields: Optional[List[str]] = None,
             exclude_fields: Optional[List[str]] = None,
             region: Optional[str] = None,
             samples: Optional[List[str]] = None,
             phased: Optional[bool] = False) -> SNPObject:
        """
        Read a vcf file into a SNPObject.

        Parameters
        ----------
        fields: '*', None or list of strings, default=None
            Fields to extract data for. This parameter specifies which data fields
            from the VCF file should be included in the result. Available options include
            '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', and 'FORMAT'.
            To extract all fields, provide just the string '*' or the default None.
        exclude_fields: None or list of strings, default=None
            Fields to exclude for use in combination with fields='*'. Available options include
            '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', and 'FORMAT'.
        region: string, default=None
            Genomic region to extract variants for. If provided, it should be a
            tabix-style region string, specifying a chromosome name and optionally
            beginning and end coordinates (e.g., '2L:100000-200000'). TODO
        samples: None, list of strings or list of ints, default=None
            Selection of samples to extract calldata for. If provided, should be
            a list of strings giving sample identifiers. May also be a list of
            integers giving indices of selected samples.  If an empty list is provided,
            no samples are extracted.
        phased: bool, default=False
            Whether to store the genotypes as phased. If True, `calldata_gt` is
            a numpy array of shape (num_variants, num_samples, 2) containing 0, 1.
            If False, `calldata_gt` is a numpy array of shape (num_variants, num_samples)
            containing 0, 1, 2.

        Returns
        -------
        snpobj: SNPObject
            SNPObject containing the data from the VCF file. The format and content
            of this object depend on the specified parameters and the content of
            the VCF file.
        """
        # TODO: add support for excluding GT

        log.info(f"Reading {self._filename}")

        try:
            # Get the names and data types for the VCF file
            names = _get_vcf_names(self._filename)
            dtype_options = _infer_data_types(names)

            # Extract columns to read based on specified 'fields', 'exclude_fields' and 'samples'
            # `selected_column_idxs` contains the indexes of the selected columns
            fields, samples, selected_column_idxs = _extract_columns(names, fields, exclude_fields, samples)

            # Read the VCF file into a Polars DataFrame
            vcf = pl.read_csv(
                self._filename,
                comment_prefix='#',
                has_header=False,
                separator='\t',
                columns=selected_column_idxs,
                dtypes=dtype_options
            )

            log.debug("vcf polars read")

            if not samples:
                genotypes = np.array([])
            else:  # note that if samples is None, all samples are read
                # Process maternal strand:
                # Extract the first position from genotype, e.g., 0|1 -> 0
                # Replace missing values codified as ".", "-", or "" with -1, necessary for integer casting
                genotype_maternal = vcf[samples].select(pl.all().str.slice(0, length=1)) \
                                                .select(pl.all().replace({
                                                    ".": -1,
                                                    "-": -1,
                                                    "": -1
                                                })).cast(pl.Int8)

                # Process paternal strand:
                # Extract the third position from genotype, e.g., 0|1 -> 1
                # Convert ":" to ".." such that if only maternal strand is present, paternal strand is set to missing,
                # e.g., 0:0.982 -> 0..0.982 -> . -> -1
                # Replace missing values with -1
                genotype_paternal = vcf[samples].select(pl.all().str.replace_all('-1', '.')) \
                                                .select(pl.all().str.replace(':', '..')) \
                                                .select(pl.all().str.slice(2, length=1)) \
                                                .select(pl.all().replace({
                                                    ".": -1,
                                                    "": -1
                                                })).cast(pl.Int8)

                # Combine maternal and paternal genotypes
                genotypes = np.dstack((genotype_maternal, genotype_paternal))

                # Sum genotypes if not phased
                if not phased:
                    genotypes = genotypes.sum(axis=2, dtype=np.int8)

            # Extract alternate alleles and create a structured array
            if 'ALT' in fields:
                variants_alt = vcf['ALT'].to_numpy()
                variants_alt = np.column_stack([variants_alt,
                                                ['']*len(variants_alt),
                                                ['']*len(variants_alt)
                                                ])
            else:
                variants_alt = np.array([])

            # Create a SNPObject with the processed data
            snpobj = SNPObject(
                calldata_gt=genotypes,
                samples=np.array(samples),
                variants_ref=vcf['REF'].to_numpy() if 'REF' in fields else np.array([]),
                variants_alt=variants_alt,
                variants_chrom=vcf['#CHROM'].to_numpy() if '#CHROM' in fields else np.array([]),
                variants_filter_pass=vcf['FILTER'].to_numpy() if 'FILTER' in fields else np.array([]),
                variants_id=vcf['ID'].to_numpy() if 'ID' in fields else np.array([]),
                variants_pos=vcf['POS'].to_numpy() if 'POS' in fields else np.array([]),
                variants_qual=vcf['QUAL'].to_numpy() if 'QUAL' in fields else np.array([])
            )

            log.info(f"Finished reading {self.filename}")

            return snpobj

        except Exception as e:
            print(f"An error occurred: {e}.")
            from snputils.snp.io.read import VCFReader

            # Instantiate a VCFReader object and read SNP data
            reader = VCFReader(self._filename)
            snpobj = reader.read()

            return snpobj
