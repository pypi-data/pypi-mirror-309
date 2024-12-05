import logging
import pathlib
import numpy as np
import copy
import warnings
import re
from typing import Any, Union, Tuple, List, Sequence, Dict, Optional

log = logging.getLogger(__name__)


class SNPObject:
    """
    A class for Single Nucleotide Polymorphism (SNP) data.
    """
    def __init__(
        self,
        calldata_gt: Optional[np.ndarray] = None,
        samples: Optional[np.ndarray] = None,
        variants_ref: Optional[np.ndarray] = None,
        variants_alt: Optional[np.ndarray] = None,
        variants_chrom: Optional[np.ndarray] = None,
        variants_filter_pass: Optional[np.ndarray] = None,
        variants_id: Optional[np.ndarray] = None,
        variants_pos: Optional[np.ndarray] = None,
        variants_qual: Optional[np.ndarray] = None
    ) -> None:
        """
        Args:
            calldata_gt (array, optional): 
                An array containing genotype data for each sample. This array can be either 2D with shape 
                `(n_snps, n_samples)` if the paternal and maternal strands are averaged, or 3D with shape 
                `(n_snps, n_samples, 2)` if the strands are kept separate.
            samples (array of shape (n_sampels,), optional): 
                An array containing unique sample identifiers.
            variants_ref (array of shape (n_snps,), optional): 
                An array containing the reference allele for each SNP.
            variants_alt (array of shape (n_snps, 3), optional): 
                An array containing the alternate alleles for each SNP.
            variants_chrom (array of shape (n_snps,), optional): 
                An array containing the chromosome for each SNP.
            variants_filter_pass (array of shape (n_snps,), optional): 
                An array indicating whether each SNP passed control checks.
            variants_id (array of shape (n_snps,), optional): 
                An array containing unique identifiers (IDs) for each SNP.
            variants_pos (array of shape (n_snps,), optional): 
                An array containing the chromosomal positions for each SNP.
            variants_qual (array of shape (n_snps,), optional): 
                An array containing the Phred-scaled quality score for each SNP.
        """
        self.__calldata_gt = calldata_gt
        self.__samples = samples
        self.__variants_ref = variants_ref
        self.__variants_alt = variants_alt
        self.__variants_chrom = variants_chrom
        self.__variants_filter_pass = variants_filter_pass
        self.__variants_id = variants_id
        self.__variants_pos = variants_pos
        self.__variants_qual = variants_qual

    def __getitem__(self, key: str) -> Any:
        """
        To access an attribute of the class using the square bracket notation,
        similar to a dictionary.
        """
        try:
            return getattr(self, key)
        except:
            raise KeyError(f'Invalid key: {key}.')

    def __setitem__(self, key: str, value: Any):
        """
        To set an attribute of the class using the square bracket notation,
        similar to a dictionary.
        """
        try:
            setattr(self, key, value)
        except:
            raise KeyError(f'Invalid key: {key}.')

    @property
    def calldata_gt(self) -> np.ndarray:
        """
        Retrieve `calldata_gt`.

        Returns:
            **array:** 
                An array containing genotype data for each sample. This array can be either 2D with shape 
                `(n_snps, n_samples)` if the paternal and maternal strands are averaged, or 3D with shape 
                `(n_snps, n_samples, 2)` if the strands are kept separate.
        """
        return self.__calldata_gt

    @calldata_gt.setter
    def calldata_gt(self, x: np.ndarray):
        """
        Update `calldata_gt`.
        """
        self.__calldata_gt = x

    @property
    def samples(self) -> Optional[np.ndarray]:
        """
        Retrieve `samples`.

        Returns:
            **array of shape (n_sampels,):** 
                An array containing unique sample identifiers.
        """
        return self.__samples

    @samples.setter
    def samples(self, x: np.ndarray):
        """
        Update `samples`.
        """
        self.__samples = x

    @property
    def variants_ref(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_ref`.

        Returns:
            **array of shape (n_snps,):** An array containing the reference allele for each SNP.
        """
        return self.__variants_ref

    @variants_ref.setter
    def variants_ref(self, x: np.ndarray):
        """
        Update `variants_ref`.
        """
        self.__variants_ref = x

    @property
    def variants_alt(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_alt`.

        Returns:
            **array of shape (n_snps, 3):** An array containing the alternate alleles for each SNP.
        """
        return self.__variants_alt

    @variants_alt.setter
    def variants_alt(self, x: np.ndarray):
        """
        Update `variants_alt`.
        """
        self.__variants_alt = x

    @property
    def variants_chrom(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_chrom`.

        Returns:
            **array of shape (n_snps,):** An array containing the chromosome for each SNP.
        """
        return self.__variants_chrom

    @variants_chrom.setter
    def variants_chrom(self, x: np.ndarray):
        """
        Update `variants_chrom`.
        """
        self.__variants_chrom = x

    @property
    def variants_filter_pass(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_filter_pass`.

        Returns:
            **array of shape (n_snps,):** An array indicating whether each SNP passed control checks.
        """
        return self.__variants_filter_pass

    @variants_filter_pass.setter
    def variants_filter_pass(self, x: np.ndarray):
        """
        Update `variants_filter_pass`.
        """
        self.__variants_filter_pass = x

    @property
    def variants_id(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_id`.

        Returns:
            **array of shape (n_snps,):** An array containing unique identifiers (IDs) for each SNP.
        """
        return self.__variants_id

    @variants_id.setter
    def variants_id(self, x: np.ndarray):
        """
        Update `variants_id`.
        """
        self.__variants_id = x

    @property
    def variants_pos(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_pos`.

        Returns:
            **array of shape (n_snps,):** An array containing the chromosomal positions for each SNP.
        """
        return self.__variants_pos

    @variants_pos.setter
    def variants_pos(self, x: np.ndarray):
        """
        Update `variants_pos`.
        """
        self.__variants_pos = x

    @property
    def variants_qual(self) -> Optional[np.ndarray]:
        """
        Retrieve `variants_qual`.

        Returns:
            **array of shape (n_snps,):** An array containing the Phred-scaled quality score for each SNP.
        """
        return self.__variants_qual

    @variants_qual.setter
    def variants_qual(self, x: np.ndarray):
        """
        Update `variants_qual`.
        """
        self.__variants_qual = x

    @property
    def n_samples(self) -> int:
        """
        Retrieve `n_samples`.

        Returns:
            **int:** The total number of samples.
        """
        return self.__calldata_gt.shape[1]

    @property
    def n_snps(self) -> int:
        """
        Retrieve `n_snps`.

        Returns:
            **int:** The total number of SNPs.
        """
        return self.__calldata_gt.shape[0]

    @property
    def n_chrom(self) -> Optional[int]:
        """
        Retrieve `n_chrom`.

        Returns:
            **int:** The total number of unique chromosomes in `variants_chrom`.
        """
        if self.variants_chrom is None:
            warnings.warn("Chromosome data `variants_chrom` is None.")
            return None

        return len(self.unique_chrom)

    @property
    def unique_chrom(self) -> Optional[np.ndarray]:
        """
        Retrieve `unique_chrom`.

        Returns:
            **array:** The unique chromosome names in `variants_chrom`, preserving their order of appearance.
        """
        if self.variants_chrom is None:
            warnings.warn("Chromosome data `variants_chrom` is None.")
            return None

        # Identify unique chromosome names and their first indexes of occurrence
        _, idx = np.unique(self.variants_chrom, return_index=True)
        # Return chromosome names sorted by their first occurrence to maintain original order
        return self.variants_chrom[np.sort(idx)]

    @property
    def is_phased(self) -> bool:
        """
        Retrieve `is_phased`.
        
        Returns:
            **bool:** True if the genotype data in `calldata_gt` has shape 
            `(n_samples, n_snps, 2)`, False if it has shape `(n_samples, n_snps)`.
        """
        if self.calldata_gt is None:
            warnings.warn("Genotype data `calldata_gt` is None.")
            return None
        
        return self.calldata_gt.ndim == 3

    def copy(self) -> 'SNPObject':
        """
        Create and return a copy of `self`.

        Returns:
            **SNPObject:** 
                A new instance of the current object.
        """
        return copy.deepcopy(self)

    def keys(self) -> List[str]:
        """
        Retrieve a list of public attribute names for `self`.

        Returns:
            **list of str:** 
                A list of attribute names, with internal name-mangling removed, 
                for easier reference to public attributes in the instance.
        """
        return [attr.replace('_SNPObject__', '') for attr in vars(self)]

    def filter_variants(
            self, 
            chrom: Optional[Union[str, Sequence[str], np.ndarray, None]] = None, 
            pos: Optional[Union[int, Sequence[int], np.ndarray, None]] = None, 
            indexes: Optional[Union[int, Sequence[int], np.ndarray, None]] = None, 
            include: bool = True, 
            inplace: bool = False
        ) -> Optional['SNPObject']:
        """
        Filter variants based on specified chromosome names, variant positions, or variant indexes.

        This method updates the `calldata_gt`, `variants_ref`, `variants_alt`, 
        `variants_chrom`, `variants_filter_pass`, `variants_id`, `variants_pos`, and 
        `variants_qual` attributes to include or exclude the specified variants. The filtering 
        criteria can be based on chromosome names, variant positions, or indexes. If multiple 
        criteria are provided, their union is used for filtering. The order of the variants is preserved.
        
        Negative indexes are supported and follow 
        [NumPy's indexing conventions](https://numpy.org/doc/stable/user/basics.indexing.html).

        Args:
            chrom (str or array_like of str, optional): 
                Chromosome(s) to filter variants by. Can be a single chromosome as a string or a sequence 
                of chromosomes. If both `chrom` and `pos` are provided, they must either have matching lengths 
                (pairing each chromosome with a position) or `chrom` should be a single value that applies to 
                all positions in `pos`. Default is None. 
            pos (int or array_like of int, optional): 
                Position(s) to filter variants by. Can be a single position as an integer or a sequence of positions. 
                If `chrom` is also provided, `pos` should either match `chrom` in length or `chrom` should be a 
                single value. Default is None.
            indexes (int or array_like of int, optional): 
                Index(es) of the variants to include or exclude. Can be a single index or a sequence
                of indexes. Negative indexes are supported. Default is None.
            include (bool, default=True): 
                If True, includes only the specified variants. If False, excludes the specified
                variants. Default is True.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the variants 
                filtered. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` with the specified variants filtered if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        if chrom is None and pos is None and indexes is None:
            raise ValueError("At least one of 'chrom', 'pos', or 'indexes' must be provided.")

        n_snps = self.n_snps

        # Convert inputs to arrays for consistency
        chrom = np.atleast_1d(chrom) if chrom is not None else None
        pos = np.atleast_1d(pos) if pos is not None else None
        indexes = np.atleast_1d(indexes) if indexes is not None else None

        # Validate chrom and pos lengths if both are provided
        if chrom is not None and pos is not None:
            if len(chrom) != len(pos) and len(chrom) > 1:
                raise ValueError(
                    "When both 'chrom' and 'pos' are provided, they must either be of the same length "
                    "or 'chrom' must be a single value."
                )

        # Create a mask for chromosome and position filtering
        mask_combined = np.zeros(n_snps, dtype=bool)
        if chrom is not None and pos is not None:
            if len(chrom) == 1:
                # Apply single chromosome to all positions in `pos`
                mask_combined = (self['variants_chrom'] == chrom[0]) & np.isin(self['variants_pos'], pos)
            else:
                # Vectorized pair matching for chrom and pos
                query_pairs = np.array(
                    list(zip(chrom, pos)),
                    dtype=[
                        ('chrom', self['variants_chrom'].dtype),
                        ('pos', self['variants_pos'].dtype)
                    ]
                )
                data_pairs = np.array(
                    list(zip(self['variants_chrom'], self['variants_pos'])),
                    dtype=[
                        ('chrom', self['variants_chrom'].dtype),
                        ('pos', self['variants_pos'].dtype)
                    ]
                )
                mask_combined = np.isin(data_pairs, query_pairs)

        elif chrom is not None:
            # Only chromosome filtering
            mask_combined = np.isin(self['variants_chrom'], chrom)
        elif pos is not None:
            # Only position filtering
            mask_combined = np.isin(self['variants_pos'], pos)

        # Create mask based on indexes if provided
        if indexes is not None:
            # Validate indexes, allowing negative indexes
            out_of_bounds_indexes = indexes[(indexes < -n_snps) | (indexes >= n_snps)]
            if out_of_bounds_indexes.size > 0:
                raise ValueError(f"One or more sample indexes are out of bounds.")

            # Handle negative indexes and check for out-of-bounds indexes
            adjusted_indexes = np.mod(indexes, n_snps)

            # Create mask for specified indexes
            mask_indexes = np.zeros(n_snps, dtype=bool)
            mask_indexes[adjusted_indexes] = True

            # Combine with `chrom` and `pos` mask using logical OR (union of all specified criteria)
            mask_combined = mask_combined | mask_indexes

        # Invert mask if `include` is False
        if not include:
            mask_combined = ~mask_combined

        # Define keys to filter
        keys = [
            'variants_ref', 'variants_alt', 'variants_chrom', 'variants_filter_pass', 
            'variants_id', 'variants_pos', 'variants_qual'
        ]

        # Apply filtering based on inplace parameter
        if inplace:
            for key in keys:
                if self[key] is not None:
                    self[key] = np.asarray(self[key])[mask_combined]
            self['calldata_gt'] = np.asarray(self['calldata_gt'])[mask_combined, ...]

            return None
        else:
            # Create A new `SNPObject` with filtered data
            snpobj = self.copy()
            for key in keys:
                if snpobj[key] is not None:
                    snpobj[key] = np.asarray(snpobj[key])[mask_combined]
            snpobj['calldata_gt'] = np.asarray(self['calldata_gt'])[mask_combined, ...]

            return snpobj

    def filter_samples(
            self, 
            samples: Optional[Union[str, Sequence[str], np.ndarray, None]] = None,
            indexes: Optional[Union[int, Sequence[int], np.ndarray, None]] = None,
            include: bool = True,
            inplace: bool = False
        ) -> Optional['SNPObject']:
        """
        Filter samples based on specified names or indexes.

        This method updates the `samples` and `calldata_gt` attributes to include or exclude the specified 
        samples. The order of the samples is preserved.

        If both samples and indexes are provided, any sample matching either a name in samples or an index in 
        indexes will be included or excluded.

        This method allows inclusion or exclusion of specific samples by their names or 
        indexes. When both sample names and indexes are provided, the union of the specified samples 
        is used. Negative indexes are supported and follow 
        [NumPy's indexing conventions](https://numpy.org/doc/stable/user/basics.indexing.html).

        Args:
            samples (str or array_like of str, optional): 
                 Name(s) of the samples to include or exclude. Can be a single sample name or a
                 sequence of sample names. Default is None.
            indexes (int or array_like of int, optional):
                Index(es) of the samples to include or exclude. Can be a single index or a sequence
                of indexes. Negative indexes are supported. Default is None.
            include (bool, default=True): 
                If True, includes only the specified samples. If False, excludes the specified
                samples. Default is True.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the samples 
                filtered. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` with the specified samples filtered if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        if samples is None and indexes is None:
            raise ValueError("At least one of 'samples' or 'indexes' must be provided.")

        n_samples = self.n_samples
        sample_names = np.array(self['samples'])

        # Create mask based on sample names
        if samples is not None:
            samples = np.atleast_1d(samples)
            mask_samples = np.isin(sample_names, samples)
            missing_samples = samples[~np.isin(samples, sample_names)]
            if missing_samples.size > 0:
                raise ValueError(f"The following specified samples were not found: {missing_samples.tolist()}")
        else:
            mask_samples = np.zeros(n_samples, dtype=bool)

        # Create mask based on sample indexes
        if indexes is not None:
            indexes = np.atleast_1d(indexes)

            # Validate indexes, allowing negative indexes
            out_of_bounds_indexes = indexes[(indexes < -n_samples) | (indexes >= n_samples)]
            if out_of_bounds_indexes.size > 0:
                raise ValueError(f"One or more sample indexes are out of bounds.")
            
            # Handle negative indexes
            adjusted_indexes = np.mod(indexes, n_samples)

            mask_indexes = np.zeros(n_samples, dtype=bool)
            mask_indexes[adjusted_indexes] = True
        else:
            mask_indexes = np.zeros(n_samples, dtype=bool)

        # Combine masks using logical OR (union of samples)
        mask_combined = mask_samples | mask_indexes

        if not include:
            mask_combined = ~mask_combined

        # Filter `samples`
        filtered_samples = sample_names[mask_combined].tolist()

        # Filter `calldata_gt`
        filtered_calldata_gt = np.array(self['calldata_gt'])[:, mask_combined, ...]

        if inplace:
            self['samples'] = filtered_samples
            self['calldata_gt'] = filtered_calldata_gt
            return None
        else:
            snpobj = self.copy()
            snpobj['samples'] = filtered_samples
            snpobj['calldata_gt'] = filtered_calldata_gt
            return snpobj

    def detect_chromosome_format(self) -> str:
        """
        Detect the chromosome naming convention in `variants_chrom` based on the prefix 
        of the first chromosome identifier in `unique_chrom`.
        
        **Recognized formats:**

        - `'chr'`: Format with 'chr' prefix, e.g., 'chr1', 'chr2', ..., 'chrX', 'chrY', 'chrM'.
        - `'chm'`: Format with 'chm' prefix, e.g., 'chm1', 'chm2', ..., 'chmX', 'chmY', 'chmM'.
        - `'chrom'`: Format with 'chrom' prefix, e.g., 'chrom1', 'chrom2', ..., 'chromX', 'chromY', 'chromM'.
        - `'plain'`: Plain format without a prefix, e.g., '1', '2', ..., 'X', 'Y', 'M'.
        
        If the format does not match any recognized pattern, `'Unknown format'` is returned.

        Returns:
            **str:** 
                A string indicating the detected chromosome format (`'chr'`, `'chm'`, `'chrom'`, or `'plain'`).
                If no recognized format is matched, returns `'Unknown format'`.
        """
        # Select the first unique chromosome identifier for format detection
        chromosome_str = self.unique_chrom[0]

        # Define regular expressions to match each recognized chromosome format
        patterns = {
            'chr': r'^chr(\d+|X|Y|M)$',    # Matches 'chr' prefixed format
            'chm': r'^chm(\d+|X|Y|M)$',    # Matches 'chm' prefixed format
            'chrom': r'^chrom(\d+|X|Y|M)$', # Matches 'chrom' prefixed format
            'plain': r'^(\d+|X|Y|M)$'       # Matches plain format without prefix
        }

        # Iterate through the patterns to identify the chromosome format
        for prefix, pattern in patterns.items():
            if re.match(pattern, chromosome_str):
                return prefix  # Return the recognized format prefix

        # If no pattern matches, return 'Unknown format'
        return 'Unknown format'

    def convert_chromosome_format(
        self, 
        from_format: str, 
        to_format: str, 
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Convert the chromosome format from one naming convention to another in `variants_chrom`.

        **Supported formats:**

        - `'chr'`: Format with 'chr' prefix, e.g., 'chr1', 'chr2', ..., 'chrX', 'chrY', 'chrM'.
        - `'chm'`: Format with 'chm' prefix, e.g., 'chm1', 'chm2', ..., 'chmX', 'chmY', 'chmM'.
        - `'chrom'`: Format with 'chrom' prefix, e.g., 'chrom1', 'chrom2', ..., 'chromX', 'chromY', 'chromM'.
        - `'plain'`: Plain format without a prefix, e.g., '1', '2', ..., 'X', 'Y', 'M'.

        Args:
            from_format (str): 
                The current chromosome format. Acceptable values are `'chr'`, `'chm'`, `'chrom'`, or `'plain'`.
            to_format (str): 
                The target format for chromosome data conversion. Acceptable values match `from_format` options.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the converted format.
                Default is False.

        Returns:
            **Optional[SNPObject]:** A new `SNPObject` with the converted chromosome format if `inplace=False`. 
            If `inplace=True`, modifies `self` in place and returns None.
        """
        # Define the list of standard chromosome identifiers
        chrom_list = [*map(str, range(1, 23)), 'X', 'Y', 'M']  # M for mitochondrial chromosomes

        # Format mappings for different chromosome naming conventions
        format_mappings = {
            'chr': [f'chr{i}' for i in chrom_list],
            'chm': [f'chm{i}' for i in chrom_list],
            'chrom': [f'chrom{i}' for i in chrom_list],
            'plain': chrom_list,
        }

        # Verify that from_format and to_format are valid naming conventions
        if from_format not in format_mappings or to_format not in format_mappings:
            raise ValueError(f"Invalid format: {from_format} or {to_format}. Must be one of {list(format_mappings.keys())}.")

        # Convert chromosomes to string for consistent comparison
        variants_chrom = self['variants_chrom'].astype(str)

        # Verify that all chromosomes in the object follow the specified `from_format`
        expected_chroms = set(format_mappings[from_format])
        mismatched_chroms = set(variants_chrom) - expected_chroms

        if mismatched_chroms:
            raise ValueError(f"The following chromosomes do not match the `from_format` '{from_format}': {mismatched_chroms}.")

        # Create conditions for selecting based on current `from_format` names
        conditions = [variants_chrom == chrom for chrom in format_mappings[from_format]]

        # Rename chromosomes based on inplace flag
        if inplace:
            self['variants_chrom'] = np.select(conditions, format_mappings[to_format], default='unknown')
            return None
        else:
            snpobject = self.copy()
            snpobject['variants_chrom'] = np.select(conditions, format_mappings[to_format], default='unknown')
            return snpobject

    def match_chromosome_format(self, snpobj: 'SNPObject', inplace: bool = False) -> Optional['SNPObject']:
        """
        Convert the chromosome format in `variants_chrom` from `self` to match the format of a reference `snpobj`.

        **Recognized formats:**

        - `'chr'`: Format with 'chr' prefix, e.g., 'chr1', 'chr2', ..., 'chrX', 'chrY', 'chrM'.
        - `'chm'`: Format with 'chm' prefix, e.g., 'chm1', 'chm2', ..., 'chmX', 'chmY', 'chmM'.
        - `'chrom'`: Format with 'chrom' prefix, e.g., 'chrom1', 'chrom2', ..., 'chromX', 'chromY', 'chromM'.
        - `'plain'`: Plain format without a prefix, e.g., '1', '2', ..., 'X', 'Y', 'M'.

        Args:
            snpobj (SNPObject): 
                The reference SNPObject whose chromosome format will be matched.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the 
                chromosome format matching that of `snpobj`. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` with matched chromosome format if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Detect the chromosome naming format of the current SNPObject
        fmt1 = self.detect_chromosome_format()
        if fmt1 == 'Unknown format':
            raise ValueError("The chromosome format of the current SNPObject is unrecognized.")
        
        # Detect the chromosome naming format of the reference SNPObject
        fmt2 = snpobj.detect_chromosome_format()
        if fmt2 == 'Unknown format':
            raise ValueError("The chromosome format of the reference SNPObject is unrecognized.")

        # Convert the current SNPObject's chromosome format to match the reference format
        return self.convert_chromosome_format(fmt1, fmt2, inplace=inplace)

    def rename_chrom(
        self,
        to_replace: Union[Dict[str, str], str, List[str]] = {'^([0-9]+)$': r'chr\1', r'^chr([0-9]+)$': r'\1'},
        value: Optional[Union[str, List[str]]] = None,
        regex: bool = True,
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Replace chromosome values in `variants_chrom` using patterns or exact matches.

        This method allows flexible chromosome replacements, using regex or exact matches, useful 
        for non-standard chromosome formats. For standard conversions (e.g., 'chr1' to '1'), 
        consider `convert_chromosome_format`.

        Args:
            to_replace (dict, str, or list of str): 
                Pattern(s) or exact value(s) to be replaced in chromosome names. Default behavior 
                transforms `<chrom_num>` to `chr<chrom_num>` or vice versa. Non-matching values 
                remain unchanged.
                - If str or list of str: Matches will be replaced with `value`.
                - If regex (bool), then any regex matches will be replaced with `value`.
                - If dict: Keys defines values to replace, with corresponding replacements as values.
            value (str or list of str, optional): 
                Replacement value(s) if `to_replace` is a string or list. Ignored if `to_replace` 
                is a dictionary.
            regex (bool, default=True): 
                If True, interprets `to_replace` keys as regex patterns.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the chromosomes
                renamed. Default is False.

        Returns:
            **Optional[SNPObject]:** A new `SNPObject` with the renamed chromosome format if `inplace=False`. 
            If `inplace=True`, modifies `self` in place and returns None.
        """
        # Standardize input format: convert `to_replace` and `value` to a dictionary if needed
        if isinstance(to_replace, (str, int)):
            to_replace = [to_replace]
        if isinstance(value, (str, int)):
            value = [value]
        if isinstance(to_replace, list) and isinstance(value, list):
            dictionary = dict(zip(to_replace, value))
        elif isinstance(to_replace, dict) and value is None:
            dictionary = to_replace
        else:
            raise ValueError(
            "Invalid input: `to_replace` and `value` must be compatible types (both str, list of str, or dict)."
        )

        # Vectorized function for replacing values in chromosome array
        vec_replace_values = np.vectorize(self._match_to_replace)

        # Rename chromosomes based on inplace flag
        if inplace:
            self.variants_chrom = vec_replace_values(self.variants_chrom, dictionary, regex)
            return None
        else:
            snpobj = self.copy()
            snpobj.variants_chrom = vec_replace_values(self.variants_chrom, dictionary, regex)
            return snpobj

    def rename_missings(
        self, 
        before: Union[int, float, str] = -1, 
        after: Union[int, float, str] = '.', 
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Replace missing values in the `calldata_gt` attribute.

        This method identifies missing values in 'calldata_gt' and replaces them with a specified 
        value. By default, it replaces occurrences of `-1` (often used to signify missing data) with `'.'`.

        Args:
            before (int, float, or str, default=-1): 
                The current representation of missing values in `calldata_gt`. Common values might be -1, '.', or NaN.
                Default is -1.
            after (int, float, or str, default='.'): 
                The value that will replace `before`. Default is '.'.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the applied 
                replacements. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` with the renamed missing values if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Rename missing values in the `calldata_gt` attribute based on inplace flag
        if inplace:
            self['calldata_gt'] = np.where(self['calldata_gt'] == before, after, self['calldata_gt'])
            return None
        else:
            snpobj = self.copy()
            snpobj['calldata_gt'] = np.where(snpobj['calldata_gt'] == before, after, snpobj['calldata_gt'])
            return snpobj

    def get_common_variants_intersection(
        self, 
        snpobj: 'SNPObject', 
        index_by: str = 'pos'
    ) -> Tuple[List[str], np.ndarray, np.ndarray]:
        """
        Identify common variants between `self` and the `snpobj` instance based on the specified `index_by` criterion, 
        which may match based on chromosome and position (`variants_chrom`, `variants_pos`), ID (`variants_id`), or both.

        This method returns the identifiers of common variants and their corresponding indices in both objects.

        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
            index_by (str, default='pos'): 
                Criteria for matching variants. Options:
                - `'pos'`: Matches by chromosome and position (`variants_chrom`, `variants_pos`), e.g., 'chr1-12345'.
                - `'id'`: Matches by variant ID alone (`variants_id`), e.g., 'rs123'.
                - `'pos+id'`: Matches by chromosome, position, and ID (`variants_chrom`, `variants_pos`, `variants_id`), e.g., 'chr1-12345-rs123'.
                Default is 'pos'.

        Returns:
            Tuple containing:
            - **list of str:** A list of common variant identifiers (as strings).
            - **array:** An array of indices in `self` where common variants are located.
            - **array:** An array of indices in `snpobj` where common variants are located.
        """
        # Create unique identifiers for each variant in both SNPObjects based on the specified criterion
        if index_by == 'pos':
            query_identifiers = [f"{chrom}-{pos}" for chrom, pos in zip(self['variants_chrom'], self['variants_pos'])]
            reference_identifiers = [f"{chrom}-{pos}" for chrom, pos in zip(snpobj['variants_chrom'], snpobj['variants_pos'])]
        elif index_by == 'id':
            query_identifiers = self['variants_id'].tolist()
            reference_identifiers = snpobj['variants_id'].tolist()
        elif index_by == 'pos+id':
            query_identifiers = [
                f"{chrom}-{pos}-{ids}" for chrom, pos, ids in zip(self['variants_chrom'], self['variants_pos'], self['variants_id'])
            ]
            reference_identifiers = [
                f"{chrom}-{pos}-{ids}" for chrom, pos, ids in zip(snpobj['variants_chrom'], snpobj['variants_pos'], snpobj['variants_id'])
            ]
        else:
            raise ValueError("`index_by` must be one of 'pos', 'id', or 'pos+id'.")

        # Convert to sets for intersection
        common_ids = set(query_identifiers).intersection(reference_identifiers)

        # Collect indices for common identifiers
        query_idx = [i for i, id in enumerate(query_identifiers) if id in common_ids]
        reference_idx = [i for i, id in enumerate(reference_identifiers) if id in common_ids]

        return list(common_ids), np.array(query_idx), np.array(reference_idx)

    def get_common_markers_intersection(
        self, 
        snpobj: 'SNPObject'
    ) -> Tuple[List[str], np.ndarray, np.ndarray]:
        """
        Identify common markers between between `self` and the `snpobj` instance. Common markers are identified 
        based on matching chromosome (`variants_chrom`), position (`variants_pos`), reference (`variants_ref`), 
        and alternate (`variants_alt`) alleles.

        This method returns the identifiers of common markers and their corresponding indices in both objects.
        
        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
        
        Returns:
            Tuple containing:
            - **list of str:** A list of common variant identifiers (as strings).
            - **array:** An array of indices in `self` where common variants are located.
            - **array:** An array of indices in `snpobj` where common variants are located.
        """
        # Generate unique identifiers based on chrom, pos, ref, and alt alleles
        query_identifiers = [
            f"{chrom}-{pos}-{ref}-{alt}" for chrom, pos, ref, alt in 
            zip(self['variants_chrom'], self['variants_pos'], self['variants_ref'], self['variants_alt'])
        ]
        reference_identifiers = [
            f"{chrom}-{pos}-{ref}-{alt}" for chrom, pos, ref, alt in 
            zip(snpobj['variants_chrom'], snpobj['variants_pos'], snpobj['variants_ref'], snpobj['variants_alt'])
        ]

        # Convert to sets for intersection
        common_ids = set(query_identifiers).intersection(reference_identifiers)

        # Collect indices for common identifiers in both SNPObjects
        query_idx = [i for i, id in enumerate(query_identifiers) if id in common_ids]
        reference_idx = [i for i, id in enumerate(reference_identifiers) if id in common_ids]

        return list(common_ids), np.array(query_idx), np.array(reference_idx)

    def subset_to_common_variants(
        self, 
        snpobj: 'SNPObject', 
        index_by: str = 'pos', 
        common_variants_intersection: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Subset `self` to include only the common variants with a reference `snpobj` based on 
        the specified `index_by` criterion, which may match based on chromosome and position 
        (`variants_chrom`, `variants_pos`), ID (`variants_id`), or both.
        
        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
            index_by (str, default='pos'): 
                Criteria for matching variants. Options:
                - `'pos'`: Matches by chromosome and position (`variants_chrom`, `variants_pos`), e.g., 'chr1-12345'.
                - `'id'`: Matches by variant ID alone (`variants_id`), e.g., 'rs123'.
                - `'pos+id'`: Matches by chromosome, position, and ID (`variants_chrom`, `variants_pos`, `variants_id`), e.g., 'chr1-12345-rs123'.
                Default is 'pos'.
            common_variants_intersection (Tuple[np.ndarray, np.ndarray], optional): 
                Precomputed indices of common variants between `self` and `snpobj`. If None, intersection is 
                computed within the function.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the common variants
                subsetted. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                Optional[SNPObject]: A new `SNPObject` with the common variants subsetted if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Get indices of common variants if not provided
        if common_variants_intersection is None:
            _, query_idx, _ = self.get_common_variants_intersection(snpobj, index_by=index_by)
        else:
            query_idx, _ = common_variants_intersection

        # Use filter_variants method with the identified indices, applying `inplace` as specified
        return self.filter_variants(indexes=query_idx, include=True, inplace=inplace)

    def subset_to_common_markers(
        self, 
        snpobj: 'SNPObject', 
        common_markers_intersection: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Subset `self` to include only the common markers with a reference `snpobj`. Common markers are identified 
        based on matching chromosome (`variants_chrom`), position (`variants_pos`), reference (`variants_ref`), 
        and alternate (`variants_alt`) alleles.

        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
            common_markers_intersection (tuple of arrays, optional): 
                Precomputed indices of common markers between `self` and `snpobj`. If None, intersection is 
                computed within the function.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the common markers
                subsetted. Default is False.

        Returns:
            **SNPObject:** 
                **Optional[SNPObject]:** A new `SNPObject` with the common markers subsetted if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Get indices of common markers if not provided
        if common_markers_intersection is None:
            _, query_idx, _ = self.get_common_markers_intersection(snpobj)
        else:
            query_idx, _ = common_markers_intersection

        # Use filter_variants method with the identified indices, applying `inplace` as specified
        return self.filter_variants(indexes=query_idx, include=True, inplace=inplace)

    def remove_strand_ambiguous_variants(self, inplace: bool = False) -> Optional['SNPObject']:
        """
        A strand-ambiguous variant has reference (`variants_ref`) and alternate (`variants_alt`) alleles 
        in the pairs A/T, T/A, C/G, or G/C, where both alleles are complementary and thus indistinguishable 
        in terms of strand orientation.

        Args:
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with the 
                strand-ambiguous variants removed. Default is False.

        Returns:
            **Optional[SNPObject]:** A new `SNPObject` with non-ambiguous variants only if `inplace=False`. 
            If `inplace=True`, modifies `self` in place and returns None.
        """
        # Identify strand-ambiguous SNPs using vectorized comparisons
        is_AT = (self['variants_ref'] == 'A') & (self['variants_alt'][:, 0] == 'T')
        is_TA = (self['variants_ref'] == 'T') & (self['variants_alt'][:, 0] == 'A')
        is_CG = (self['variants_ref'] == 'C') & (self['variants_alt'][:, 0] == 'G')
        is_GC = (self['variants_ref'] == 'G') & (self['variants_alt'][:, 0] == 'C')

        # Create a combined mask for all ambiguous variants
        ambiguous_mask = is_AT | is_TA | is_CG | is_GC
        non_ambiguous_idx = np.where(~ambiguous_mask)[0]

        # Count each type of ambiguity using numpy's sum on boolean arrays
        A_T_count = np.sum(is_AT)
        T_A_count = np.sum(is_TA)
        C_G_count = np.sum(is_CG)
        G_C_count = np.sum(is_GC)

        # Log the counts of each type of strand-ambiguous variants
        total_ambiguous = A_T_count + T_A_count + C_G_count + G_C_count
        log.info(f'{A_T_count} ambiguities of A-T type.')
        log.info(f'{T_A_count} ambiguities of T-A type.')
        log.info(f'{C_G_count} ambiguities of C-G type.')
        log.info(f'{G_C_count} ambiguities of G-C type.')

        # Filter out ambiguous variants and keep non-ambiguous ones
        log.debug(f'Removing {total_ambiguous} strand-ambiguous variants...')
        return self.filter_variants(indexes=non_ambiguous_idx, include=True, inplace=inplace)

    def correct_flipped_variants(
        self, 
        snpobj: 'SNPObject', 
        check_complement: bool = True, 
        index_by: str = 'pos', 
        common_variants_intersection: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        log_stats: bool = True,
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Correct flipped variants between between `self` and a reference `snpobj`, where reference (`variants_ref`) 
        and alternate (`variants_alt`) alleles are swapped.

        **Flip Detection Based on `check_complement`:**

        - If `check_complement=False`, only direct allele swaps are considered:
            1. **Direct Swap:** `self.variants_ref == snpobj.variants_alt` and `self.variants_alt == snpobj.variants_ref`.

        - If `check_complement=True`, both direct and complementary swaps are considered, with four possible cases:
            1. **Direct Swap:** `self.variants_ref == snpobj.variants_alt` and `self.variants_alt == snpobj.variants_ref`.
            2. **Complement Swap of Ref:** `complement(self.variants_ref) == snpobj.variants_alt` and `self.variants_alt == snpobj.variants_ref`.
            3. **Complement Swap of Alt:** `self.variants_ref == snpobj.variants_alt` and `complement(self.variants_alt) == snpobj.variants_ref`.
            4. **Complement Swap of both Ref and Alt:** `complement(self.variants_ref) == snpobj.variants_alt` and `complement(self.variants_alt) == snpobj.variants_ref`.

        **Note:** Variants where `self.variants_ref == self.variants_alt` are ignored as they are ambiguous.

        **Correction Process:** 
        - Swaps `variants_ref` and `variants_alt` alleles in `self` to align with `snpobj`.
        - Flips `calldata_gt` values (0 becomes 1, and 1 becomes 0) to match the updated allele configuration.

        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
            check_complement (bool, default=True): 
                If True, also checks for complementary base pairs (A/T, T/A, C/G, and G/C) when identifying swapped variants.
                Default is True.
            index_by (str, default='pos'): 
                Criteria for matching variants. Options:
                - `'pos'`: Matches by chromosome and position (`variants_chrom`, `variants_pos`), e.g., 'chr1-12345'.
                - `'id'`: Matches by variant ID alone (`variants_id`), e.g., 'rs123'.
                - `'pos+id'`: Matches by chromosome, position, and ID (`variants_chrom`, `variants_pos`, `variants_id`), e.g., 'chr1-12345-rs123'.
                Default is 'pos'.
            common_variants_intersection (tuple of arrays, optional): 
                Precomputed indices of common variants between `self` and `snpobj`. If None, intersection is 
                computed within the function.
            log_stats (bool, default=True): 
                If True, logs statistical information about matching and ambiguous alleles. Default is True.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with corrected 
                flips. Default is False.

        Returns:
            **Optional[SNPObject]**: 
                A new `SNPObject` with corrected flips if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Define complement mappings for nucleotides
        complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

        # Helper function to get the complement of a base
        def get_complement(base: str) -> str:
            return complement_map.get(base, base)

        # Get common variant indices if not provided
        if common_variants_intersection != None:
            query_idx, reference_idx = common_variants_intersection
        else:
            _, query_idx, reference_idx = self.get_common_variants_intersection(snpobj, index_by=index_by)

        # Log statistics on matching alleles if enabled
        if log_stats:
            matching_ref = np.sum(self['variants_ref'][query_idx] == snpobj['variants_ref'][reference_idx])
            matching_alt = np.sum(self['variants_alt'][query_idx, 0] == snpobj['variants_alt'][reference_idx, 0])
            ambiguous = np.sum(self['variants_ref'][query_idx] == self['variants_alt'][query_idx, 0])
            log.info(f"Matching reference alleles (ref=ref'): {matching_ref}, Matching alternate alleles (alt=alt'): {matching_alt}.")
            log.info(f"Number of ambiguous alleles (ref=alt): {ambiguous}.")

        # Identify indices where `ref` and `alt` alleles are swapped
        if not check_complement:
            # Simple exact match for swapped alleles
            swapped_ref = (self['variants_ref'][query_idx] == snpobj['variants_alt'][reference_idx, 0])
            swapped_alt = (self['variants_alt'][query_idx, 0] == snpobj['variants_ref'][reference_idx])
        else:
            # Check for swapped or complementary-swapped alleles
            swapped_ref = (
                (self['variants_ref'][query_idx] == snpobj['variants_alt'][reference_idx, 0]) |
                (np.vectorize(get_complement)(self['variants_ref'][query_idx]) == snpobj['variants_alt'][reference_idx, 0])
            )
            swapped_alt = (
                (self['variants_alt'][query_idx, 0] == snpobj['variants_ref'][reference_idx]) |
                (np.vectorize(get_complement)(self['variants_alt'][query_idx, 0]) == snpobj['variants_ref'][reference_idx])
            )

        # Filter out ambiguous variants where `ref` and `alt` alleles match (ref=alt)
        not_ambiguous = (self['variants_ref'][query_idx] != self['variants_alt'][query_idx, 0])

        # Indices in `self` of flipped variants
        flip_idx_query = query_idx[swapped_ref & swapped_alt & not_ambiguous]

        # Correct the identified variant flips
        if len(flip_idx_query) > 0:
            log.info(f'Correcting {len(flip_idx_query)} variant flips...')

            temp_alts = self['variants_alt'][flip_idx_query, 0]
            temp_refs = self['variants_ref'][flip_idx_query]

            # Correct the variant flips based on whether the operation is in-place or not
            if inplace:
                self['variants_alt'][flip_idx_query, 0] = temp_refs
                self['variants_ref'][flip_idx_query] = temp_alts
                self['calldata_gt'][flip_idx_query] = 1 - self['calldata_gt'][flip_idx_query]
                return None
            else:
                snpobj = self.copy()
                snpobj['variants_alt'][flip_idx_query, 0] = temp_refs
                snpobj['variants_ref'][flip_idx_query] = temp_alts
                snpobj['calldata_gt'][flip_idx_query] = 1 - snpobj['calldata_gt'][flip_idx_query]
                return snpobj
        else:
            log.info('No variant flips found to correct.')
            return self if not inplace else None

    def remove_mismatching_variants(
        self, 
        snpobj: 'SNPObject', 
        index_by: str = 'pos', 
        common_variants_intersection: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        inplace: bool = False
    ) -> Optional['SNPObject']:
        """
        Remove variants from `self`, where reference (`variants_ref`) and/or alternate (`variants_alt`) alleles 
        do not match with a reference `snpobj`.

        Args:
            snpobj (SNPObject): 
                The reference SNPObject to compare against.
            index_by (str, default='pos'): 
                Criteria for matching variants. Options:
                - `'pos'`: Matches by chromosome and position (`variants_chrom`, `variants_pos`), e.g., 'chr1-12345'.
                - `'id'`: Matches by variant ID alone (`variants_id`), e.g., 'rs123'.
                - `'pos+id'`: Matches by chromosome, position, and ID (`variants_chrom`, `variants_pos`, `variants_id`), e.g., 'chr1-12345-rs123'.
                Default is 'pos'.
            common_variants_intersection (tuple of arrays, optional): 
                Precomputed indices of common variants between `self` and the reference `snpobj`.
                If None, the intersection is computed within the function.
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` without 
                mismatching variants. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` without mismatching variants if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Get common variant indices if not provided
        if common_variants_intersection is not None:
            query_idx, reference_idx = common_variants_intersection
        else:
            _, query_idx, reference_idx = self.get_common_variants_intersection(snpobj, index_by=index_by)

        # Vectorized comparison of `ref` and `alt` alleles
        ref_mismatch = self['variants_ref'][query_idx] != snpobj['variants_ref'][reference_idx]
        alt_mismatch = self['variants_alt'][query_idx, 0] != snpobj['variants_alt'][reference_idx, 0]
        mismatch_mask = ref_mismatch | alt_mismatch

        # Identify indices in `self` of mismatching variants
        mismatch_idx = query_idx[mismatch_mask]

        # Compute total number of variant mismatches
        total_mismatches = np.sum(mismatch_mask)

        # Filter out mismatching variants
        log.debug(f'Removing {total_mismatches} mismatching variants...')
        return self.filter_variants(indexes=mismatch_idx, include=True, inplace=inplace)

    def shuffle_variants(self, inplace: bool = False) -> Optional['SNPObject']:
        """
        Randomly shuffle the positions of variants in the SNPObject, ensuring that all associated 
        data (e.g., `calldata_gt` and variant-specific attributes) remain aligned.

        Args:
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with 
                shuffled variants. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` without shuffled variant positions if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        # Generate a random permutation index for shuffling variant positions
        shuffle_index = np.random.permutation(self.n_snps)

        # Apply shuffling to all relevant attributes using the class's dictionary-like interface
        if inplace:
            for key in self.keys():
                if self[key] is not None:
                    if key == 'calldata_gt':
                        # `calldata_gt`` has a different shape, so it's shuffled along axis 0
                        self[key] = self[key][shuffle_index, ...]
                    elif 'variant' in key:
                        # Other attributes are 1D arrays
                        self[key] = np.asarray(self[key])[shuffle_index]
            return None
        else:
            shuffled_snpobj = self.copy()
            for key in shuffled_snpobj.keys():
                if shuffled_snpobj[key] is not None:
                    if key == 'calldata_gt':
                        shuffled_snpobj[key] = shuffled_snpobj[key][shuffle_index, ...]
                    elif 'variant' in key:
                        shuffled_snpobj[key] = np.asarray(shuffled_snpobj[key])[shuffle_index]
            return shuffled_snpobj

    def set_empty_to_missing(self, inplace: bool = False) -> Optional['SNPObject']:
        """
        Replace empty strings `''` with missing values `'.'` in attributes of `self`.

        Args:
            inplace (bool, default=False): 
                If True, modifies `self` in place. If False, returns a new `SNPObject` with empty 
                strings `''` replaced by missing values `'.'`. Default is False.

        Returns:
            **Optional[SNPObject]:** 
                A new `SNPObject` with empty strings replaced if `inplace=False`. 
                If `inplace=True`, modifies `self` in place and returns None.
        """
        if inplace:
            if self.variants_alt is not None:
                self.variants_alt[:, 0][self.variants_alt[:, 0] == ''] = '.'
            if self.variants_ref is not None:
                self.variants_ref[self.variants_ref == ''] = '.'
            if self.variants_qual is not None:
                self.variants_qual = self.variants_qual.astype(str)
                self.variants_qual[(self.variants_qual == '') | (self.variants_qual == 'nan')] = '.'
            if self.variants_chrom is not None:
                self.variants_chrom = self.variants_chrom.astype(str)
                self.variants_chrom[self.variants_chrom == ''] = '.'
            if self.variants_filter_pass is not None:
                self.variants_filter_pass[self.variants_filter_pass == ''] = '.'
            if self.variants_id is not None:
                self.variants_id[self.variants_id == ''] = '.'
            return self
        else:
            snpobj = self.copy()
            if snpobj.variants_alt is not None:
                snpobj.variants_alt[:, 0][snpobj.variants_alt[:, 0] == ''] = '.'
            if snpobj.variants_ref is not None:
                snpobj.variants_ref[snpobj.variants_ref == ''] = '.'
            if snpobj.variants_qual is not None:
                snpobj.variants_qual = snpobj.variants_qual.astype(str)
                snpobj.variants_qual[(snpobj.variants_qual == '') | (snpobj.variants_qual == 'nan')] = '.'
            if snpobj.variants_chrom is not None:
                snpobj.variants_chrom[snpobj.variants_chrom == ''] = '.'
            if snpobj.variants_filter_pass is not None:
                snpobj.variants_filter_pass[snpobj.variants_filter_pass == ''] = '.'
            if snpobj.variants_id is not None:
                snpobj.variants_id[snpobj.variants_id == ''] = '.'
            return snpobj

    def save(self, file: Union[str, pathlib.Path]) -> None:
        """
        Save the data stored in `self` to a specified file.

        The format of the saved file is determined by the file extension provided in the `file` 
        argument. Supported formats are:
        
        - `.bed`: Binary PED (Plink) format.
        - `.pgen`: Plink2 binary genotype format.
        - `.vcf`: Variant Call Format.
        - `.pkl`: Pickle format for saving `self` in serialized form.

        Args:
            file (str or pathlib.Path): 
                The path to the file where the data will be saved. The extension of the file determines the save format. 
                Supported extensions: `.bed`, `.pgen`, `.vcf`, `.pkl`.
        """
        ext = pathlib.Path(file).suffix.lower()
        if ext == '.bed':
            self.save_bed(file)
        elif ext == '.pgen':
            self.save_pgen(file)
        elif ext == '.vcf':
            self.save_vcf(file)
        elif ext == '.pkl':
            self.save_pickle(file)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def save_bed(self, file: Union[str, pathlib.Path]) -> None:
        """
        Save the data stored in `self` to a `.bed` file.

        Args:
            file (str or pathlib.Path): 
                The path to the file where the data will be saved. It should end with `.bed`. 
                If the provided path does not have this extension, it will be appended.
        """
        from snputils.snp.io.write.bed import BEDWriter
        writer = BEDWriter(snpobj=self, filename=file)
        writer.write()

    def save_pgen(self, file: Union[str, pathlib.Path]) -> None:
        """
        Save the data stored in `self` to a `.pgen` file.

        Args:
            file (str or pathlib.Path): 
                The path to the file where the data will be saved. It should end with `.pgen`. 
                If the provided path does not have this extension, it will be appended.
        """
        from snputils.snp.io.write.pgen import PGENWriter
        writer = PGENWriter(snpobj=self, filename=file)
        writer.write()

    def save_vcf(self, file: Union[str, pathlib.Path]) -> None:
        """
        Save the data stored in `self` to a `.vcf` file.

        Args:
            file (str or pathlib.Path): 
                The path to the file where the data will be saved. It should end with `.vcf`. 
                If the provided path does not have this extension, it will be appended.
        """
        from snputils.snp.io.write.vcf import VCFWriter
        writer = VCFWriter(snpobj=self, filename=file)
        writer.write()

    def save_pickle(self, file: Union[str, pathlib.Path]) -> None:
        """
        Save `self` in serialized form to a `.pkl` file.

        Args:
            file (str or pathlib.Path): 
                The path to the file where the data will be saved. It should end with `.pkl`. 
                If the provided path does not have this extension, it will be appended.
        """
        import pickle
        with open(file, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def _match_to_replace(val: Union[str, int, float], dictionary: Dict[Any, Any], regex: bool = True) -> Union[str, int, float]:
        """
        Find a matching key in the provided dictionary for the given value `val`
        and replace it with the corresponding value.

        Args:
            val (str, int, or float): 
                The value to be matched and potentially replaced.
            dictionary (Dict): 
                A dictionary containing keys and values for matching and replacement.
                The keys should match the data type of `val`.
            regex (bool): 
                If True, interprets keys in `dictionary` as regular expressions.
                Default is True.

        Returns:
            str, int, or float: 
                The replacement value from `dictionary` if a match is found; otherwise, the original `val`.
        """
        if regex:
            # Use regular expression matching to find replacements
            for key, value in dictionary.items():
                if isinstance(key, str):
                    match = re.match(key, val)
                    if match:
                        # Replace using the first matching regex pattern
                        return re.sub(key, value, val)
            # Return the original value if no regex match is found
            return val
        else:
            # Return the value for `val` if present in `dictionary`; otherwise, return `val`
            return dictionary.get(val, val)

    @staticmethod
    def _get_chromosome_number(chrom_string: str) -> Union[int, str]:
        """
        Extracts the chromosome number from the given chromosome string.

        Args:
            chrom_string (str): 
                The chromosome identifier.

        Returns:
            int or str: 
                The numeric representation of the chromosome if detected. 
                Returns 10001 for 'X' or 'chrX', 10002 for 'Y' or 'chrY', 
                and the original `chrom_string` if unrecognized.
        """
        if chrom_string.isdigit():
            return int(chrom_string)
        else:
            chrom_num = re.search(r'\d+', chrom_string)
            if chrom_num:
                return int(chrom_num.group())
            elif chrom_string.lower() in ['x', 'chrx']:
                return 10001
            elif chrom_string.lower() in ['y', 'chry']:
                return 10002
            else:
                log.warning(f"Chromosome nomenclature not standard. Chromosome: {chrom_string}")
                return chrom_string
