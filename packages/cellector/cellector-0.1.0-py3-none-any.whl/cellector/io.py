from typing import List, Union, Dict, Optional, Tuple
from pathlib import Path
import shutil
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import numpy as np
from .utils import transpose, cat_planes
from .roi_processor import RoiProcessor


def _get_pixel_data_single(mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Get pixel data from a single mask.

    Extracts the intensity values, y-coordinates, and x-coordinates from a single mask
    footprint with intensity values.

    Parameters
    ----------
    mask : np.ndarray
        A 2D mask footprint with intensity values.

    Returns
    -------
    lam, ypix, xpix : tuple of np.ndarrays
        Intensity values, y-coordinates, and x-coordinates for the mask.
    """
    ypix, xpix = np.where(mask)
    lam = mask[ypix, xpix]
    return lam, ypix, xpix


def get_pixel_data(mask_volume, verbose: bool = True):
    """Get pixel data from a mask volume.

    Extracts the intensity values, y-coordinates, and x-coordinates from a mask volume
    where each slice of the volume corresponds to a single ROI.

    Parameters
    ----------
    mask_volume : np.ndarray
        A 3D mask volume with shape (num_rois, height, width) where each slice is a mask
        footprint with intensity values.
    verbose : bool, optional
        Whether to use a tqdm progress bar to show progress. Default is True.

    Returns
    -------
    stats : list of dict
        List of dictionaries with keys "lam", "ypix", and "xpix" for each ROI.
    """
    n_workers = max(2, cpu_count() - 2)
    try:
        with Pool(n_workers) as pool:
            iterable = tqdm(mask_volume, desc="Extracting mask data", leave=False) if verbose else mask_volume
            results = list(pool.imap(_get_pixel_data_single, iterable))

    except Exception as e:
        if "pool" in locals():
            pool.terminate()
            pool.join()
        raise e from None

    lam, ypix, xpix = transpose(results)
    stats = [dict(lam=l, ypix=y, xpix=x) for l, y, x in zip(lam, ypix, xpix)]
    return stats


def get_s2p_data(s2p_folders: List[Path], reference_key: str = "meanImg_chan2"):
    """Get list of stats and chan2 reference images from all planes in a suite2p directory.

    suite2p saves the statistics and reference images for each plane in separate
    directories. This function reads the statistics and reference images for each plane
    and returns them as lists.

    Parameters
    ----------
    s2p_folders : list of Path
        List of directories that contain the suite2p output for each plane (stat.npy and ops.npy).
    reference_key : str, optional
        Key to use for the reference image. Default is "meanImg_chan2".

    Returns
    -------
    stats : list of list of dictionaries
        Each element of stats is a list of dictionaries containing ROI statistics for each plane.
    references : list of np.ndarrays
        Each element of references is an image (usually of average red fluorescence) for each plane.
    """
    stats = []
    references = []
    for folder in s2p_folders:
        stats.append(np.load(folder / "stat.npy", allow_pickle=True))
        ops = np.load(folder / "ops.npy", allow_pickle=True).item()
        if reference_key not in ops:
            raise ValueError(f"Reference key ({reference_key}) not found in ops.npy file ({folder / 'ops.npy'})!")
        references.append(ops[reference_key])
    if not all(ref.shape == references[0].shape for ref in references):
        raise ValueError("Reference images must have the same shape as each other!")
    if not all(ref.ndim == 2 for ref in references):
        raise ValueError("Reference images must be 2D arrays!")
    return stats, references


def get_s2p_redcell(s2p_folders: List[Path]):
    """Get red cell probability masks from all planes in a suite2p directory.

    Extracts the red cell probability masks from each plane in a suite2p directory
    and returns them as a list of numpy arrays. The red cell probability masks are
    saved in the "redcell.npy" file in each plane directory in which the first column
    is a red cell assigment and the second column is the probability of each ROI being
    a red cell.

    Parameters
    ----------
    s2p_folders : list of Path
        List of directories that contain the suite2p output for each plane (redcell.npy).

    Returns
    -------
    redcell : list of np.ndarrays
        List of red cell probabilities for each plane. Each array has length N corresponding
        to the number of ROIs in that plane.
    """
    redcell = []
    for folder in s2p_folders:
        if not (folder / "redcell.npy").exists():
            raise FileNotFoundError(f"Could not find redcell.npy file in {folder}!")
        c_redcell = np.load(folder / "redcell.npy")
        redcell.append(c_redcell[:, 1])
    return redcell


class Suite2pLoader:
    def __init__(self, s2p_dir: Union[Path, str], reference_key: str = "meanImg_chan2", use_redcell: bool = True):

        self.s2p_dir = Path(s2p_dir)
        self.reference_key = reference_key

        # Get s2p folders, roi and reference data, and redcell data if it exists
        self.get_s2p_folders()
        self.num_planes = len(self.folders)
        self.stats, self.references = get_s2p_data(self.folders, reference_key=self.reference_key)
        self.rois_per_plane = [len(stat) for stat in self.stats]

        # Get redcell data if it exists
        if use_redcell:
            self.redcell = get_s2p_redcell(self.folders)

    def get_s2p_folders(self):
        """Get list of directories for each plane in a suite2p directory.

        Parameters
        ----------
        s2p_dir : Path
            Path to the suite2p directory, which contains directories for each plane in the
            format "plane0", "plane1", etc.

        Returns
        -------
        planes : list of Path
            List of directories for each plane in the suite2p directory.
        has_planes : bool
            Whether the suite2p directory contains directories for each plane.
        """
        planes = self.s2p_dir.glob("plane*")
        if planes:
            self.has_planes = True
            self.folders = list(planes)

            # Make sure all relevant files are present
            if not all(folder.is_dir() for folder in self.folders):
                raise FileNotFoundError(f"Could not find all plane directories in {self.s2p_dir}!")
            if not all((folder / "stat.npy").exists() for folder in self.folders):
                raise FileNotFoundError(f"Could not find stat.npy files in each folder {self.s2p_dir}!")
            if not all((folder / "ops.npy").exists() for folder in self.folders):
                raise FileNotFoundError(f"Could not find any ops.npy files in {self.s2p_dir}!")

        # If stat.npy and ops.py are in the s2p_dir itself, assume it's a single plane without a plane folder
        elif (self.s2p_dir / "stat.npy").exists() and (self.s2p_dir / "ops.npy").exists():
            self.has_planes = False
            self.folders = [self.s2p_dir]

        else:
            raise FileNotFoundError(f"Could not find any plane directories or stat.npy / ops.npy files in {self.s2p_dir}!")


def create_from_suite2p(
    suite2p_dir: Union[Path, str],
    use_redcell: bool = True,
    reference_key: str = "meanImg_chan2",
    extra_features: dict = {},
    autocompute: bool = True,
    clear_existing: bool = False,
):
    """Create a RoiProcessor object from a suite2p directory.

    Parameters
    ----------
    suite2p_dir : Path or str
        Path to the suite2p directory.
    use_redcell : bool, optional
        Whether to load redcell data from suite2p folders. Default is True.
    reference_key : str, optional
        Key to use for reference images in the suite2p folders. Default is "meanImg_chan2".
    extra_features : dict, optional
        Extra features to add to the RoiProcessor object. Default is empty.
    autocompute : bool, optional
        Whether to automatically compute all features for the RoiProcessor object. Default is True.

    Returns
    -------
    roi_processor : RoiProcessor
        RoiProcessor object with suite2p masks and reference images loaded that uses the suite2p_dir as the root directory.
    """
    if clear_existing:
        clear_cellector_files(suite2p_dir)

    s2p_data = Suite2pLoader(suite2p_dir, use_redcell=use_redcell, reference_key=reference_key)
    if s2p_data.redcell is not None:
        extra_features["red_s2p"] = s2p_data.redcell

    # Build data in appropriate format for RoiProcessor
    stats = cat_planes(s2p_data.stats)
    references = np.stack(s2p_data.references)
    plane_idx = np.repeat(np.arange(s2p_data.num_planes), s2p_data.rois_per_plane)

    # Initialize roi_processor object with suite2p data
    return RoiProcessor(suite2p_dir, stats, references, plane_idx, extra_features=extra_features, autocompute=autocompute)


def create_from_mask_volume(
    root_dir: Union[Path, str],
    mask_volume: np.ndarray,
    references: np.ndarray,
    plane_idx: np.ndarray,
    extra_features: dict = {},
    autocompute: bool = True,
    clear_existing: bool = False,
):
    """Create a RoiProcessor object

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory which will be used for saving results.
    mask_volume : np.ndarray
        A 3D mask volume with shape (num_rois, height, width) where each slice is a mask
        footprint with intensity values and zeros elsewhere.
    references : np.ndarray
        A 3D reference volume with shape (num_planes, height, width) where each slice is a reference
        image for a plane containing the fluorescence values to compare masks to.
    plane_idx : np.ndarray
        A 1D array of plane indices for each ROI in the mask volume.
    extra_features : dict, optional
        Extra features to add to the RoiProcessor object. Default is empty.
    autocompute : bool, optional
        Whether to automatically compute all features for the RoiProcessor object. Default is True.

    Returns
    -------
    roi_processor : RoiProcessor
        RoiProcessor object with roi masks and reference data loaded.
    """
    if clear_existing:
        clear_cellector_files(root_dir)
    stats = get_pixel_data(mask_volume)
    return RoiProcessor(root_dir, stats, references, plane_idx, extra_features=extra_features, autocompute=autocompute)


def create_from_pixel_data(
    root_dir: Union[Path, str],
    stats: List[dict],
    references: np.ndarray,
    plane_idx: np.ndarray,
    extra_features: dict = {},
    autocompute: bool = True,
    clear_existing: bool = False,
):
    """Create a RoiProcessor object

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory which will be used for saving results.
    stats : List[dict]
        List of dictionaries with keys "lam", "ypix", and "xpix" for each ROI containing the intensity values,
        y-coordinates, and x-coordinates for each ROI.
    references : np.ndarray
        A 3D reference volume with shape (num_planes, height, width) where each slice is a reference
        image for a plane containing the fluorescence values to compare masks to.
    plane_idx : np.ndarray
        A 1D array of plane indices for each ROI in the mask volume.
    extra_features : dict, optional
        Extra features to add to the RoiProcessor object. Default is empty.
    autocompute : bool, optional
        Whether to automatically compute all features for the RoiProcessor object. Default is True.

    Returns
    -------
    roi_processor : RoiProcessor
        RoiProcessor object with roi masks and reference data loaded.
    """
    if clear_existing:
        clear_cellector_files(root_dir)
    return RoiProcessor(root_dir, stats, references, plane_idx, extra_features=extra_features, autocompute=autocompute)


def get_save_directory(root_dir: Union[Path, str]):
    """Get the cellector save directory from a root folder.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.

    Returns
    -------
    save_dir : Path
        Path to the save directory for the root directory.
    """
    return Path(root_dir) / "cellector"


def clear_cellector_files(root_dir: Union[Path, str]):
    """Clear all files in the cellector save directory for a root directory.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    """
    save_dir = get_save_directory(root_dir)
    if save_dir.exists():
        for file in save_dir.glob("*"):
            file.unlink()
        save_dir.rmdir()


def propagate_criteria(root_dir: Union[Path, str], *target_dirs: Union[Path, str]):
    """Copy feature criteria saved under root_dir to other directories.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory where the feature criteria are saved.
    target_dirs : list of Path or str
        List of directories to copy the feature criteria to.

    Returns
    -------
    successful_copies : dict
        Dictionary of successful copies with the target directory as the key and a list of copied files as the value.
    unsuccessful_copies : dict
        Dictionary of unsuccessful copies with the target directory as the key and the error as the value.
    """
    if not target_dirs:
        raise ValueError("No directories to copy feature criteria to!")

    save_dir = get_save_directory(root_dir)
    copy_dirs = [get_save_directory(target_dir) for target_dir in target_dirs]
    successful_copies = {}
    unsuccessful_copies = {}
    for copy_dir in copy_dirs:
        copy_dir.mkdir(exist_ok=True)
        successful_copies[copy_dir] = []
        try:
            for file in save_dir.glob("*_criteria.npy"):
                shutil.copy(file, copy_dir / file.name)
                successful_copies[copy_dir].append(file.name)
        except Exception as e:
            # remove incomplete files from failed copy
            for file in successful_copies[copy_dir]:
                (copy_dir / file).unlink()
            unsuccessful_copies[copy_dir] = e
    return successful_copies, unsuccessful_copies


def save_feature(root_dir: Union[Path, str], name: str, feature: np.ndarray):
    """Save a feature to disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature to save.
    feature : np.ndarray
        Feature data to save to disk.
    """
    save_dir = get_save_directory(root_dir)
    save_dir.mkdir(exist_ok=True)
    np.save(save_dir / f"{name}.npy", feature)


def load_saved_feature(root_dir: Union[Path, str], name: str):
    """Load a feature from disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature to load.

    Returns
    -------
    feature : np.ndarray
        Feature data loaded from disk.
    """
    save_dir = get_save_directory(root_dir)
    return np.load(save_dir / f"{name}.npy")


def is_feature_saved(root_dir: Union[Path, str], name: str):
    """Check if a feature exists on disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature to check.

    Returns
    -------
    exists : bool
        Whether the feature exists on disk.
    """
    save_dir = get_save_directory(root_dir)
    return (save_dir / f"{name}.npy").exists()


def save_criteria(root_dir: Union[Path, str], name: str, criteria: np.ndarray):
    """Save a feature criterion to disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature criterion to save.
    criteria : np.ndarray
        Criterion data to save to disk.
    """
    save_dir = get_save_directory(root_dir)
    save_dir.mkdir(exist_ok=True)
    np.save(save_dir / f"{name}_criteria.npy", criteria)


def load_saved_criteria(root_dir: Union[Path, str], name: str):
    """Load a feature criterion from disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature criterion to load.

    Returns
    -------
    criterion : np.ndarray
        Criterion data loaded from disk.
    """
    save_dir = get_save_directory(root_dir)
    return np.load(save_dir / f"{name}_criteria.npy", allow_pickle=True)


def is_criteria_saved(root_dir: Union[Path, str], name: str):
    """Check if a feature criterion exists on disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    name : str
        Name of the feature criterion to check.

    Returns
    -------
    exists : bool
        Whether the feature criterion exists on disk.
    """
    save_dir = get_save_directory(root_dir)
    return (save_dir / f"{name}_criteria.npy").exists()


def save_manual_selection(root_dir: Union[Path, str], manual_selection: np.ndarray):
    """Save manual selection labels to disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.
    manual_selection : np.ndarray
        Manual selection labels to save to disk.
    """
    save_dir = get_save_directory(root_dir)
    save_dir.mkdir(exist_ok=True)
    np.save(save_dir / "manual_selection.npy", manual_selection)


def load_manual_selection(root_dir: Union[Path, str]):
    """Load manual selection labels from disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.

    Returns
    -------
    manual_selection : np.ndarray
        Manual selection labels loaded from disk.
    """
    save_dir = get_save_directory(root_dir)
    return np.load(save_dir / "manual_selection.npy")


def is_manual_selection_saved(root_dir: Union[Path, str]):
    """Check if manual selection labels exist on disk.

    Parameters
    ----------
    root_dir : Path or str
        Path to the root directory.

    Returns
    -------
    exists : bool
        Whether manual selection labels exist on disk.
    """
    save_dir = get_save_directory(root_dir)
    return (save_dir / "manual_selection.npy").exists()


def save_selection(
    roi_processor: RoiProcessor,
    idx_selection: np.ndarray,
    criteria: Dict[str, list],
    manual_selection: Optional[np.ndarray] = None,
):
    """Save roi processor features, criterion, and selection to disk.

    Parameters
    ----------
    roi_processor : RoiProcessor
        RoiProcessor object with features and folders to save to.
    idx_selection : np.ndarray
        Selection indices for each ROI. Should be a numpy array with shape (num_rois,) where each value is a boolean indicating
        whether the ROI is selected my meeting all feature criteria.
    criteria : Dict[str, list]
        Dictionary of feature criteria for each feature. Each value in the dictionary should be a 2 element list containing
        the minimum and maximum values for the feature. If the minimum or maximum cutoff is ignored, then that value should
        be set to None.
    manual_selection : np.ndarray
        Manual selection labels for each ROI. Shape should be (num_rois, 2), where the first column is the manual label
        and the second column is whether or not to use a manual label for that cell.
    """
    # Check that everything has the expected shapes
    if idx_selection.shape[0] != roi_processor.num_rois:
        raise ValueError(f"Selection indices have shape {idx_selection.shape} but expected {roi_processor.num_rois}!")
    if manual_selection is not None:
        if (manual_selection.shape[0] != roi_processor.num_rois) or (manual_selection.shape[1] != 2):
            raise ValueError(f"Manual selection labels have shape {manual_selection.shape} but expected ({roi_processor.num_rois}, 2)!")
    for name, value in criteria.items():
        if name not in roi_processor.features:
            raise ValueError(f"Feature {name} not found in roi_processor features!")
        if len(value) != 2:
            raise ValueError(f"Feature criteria {name} has shape {value.shape} but expected (2,)!")
    if any(feature not in criteria for feature in roi_processor.features):
        raise ValueError(f"Feature criteria missing for features: {set(roi_processor.features) - set(criteria)}!")

    # Load and create save directory
    save_dir = get_save_directory(roi_processor.root_dir)
    save_dir.mkdir(exist_ok=True)

    # Save features values for each plane
    for name, values in roi_processor.features.items():
        save_feature(roi_processor.root_dir, name, values)
    if manual_selection is not None:
        save_manual_selection(roi_processor.root_dir, manual_selection)

    # Save selection indices
    np.save(save_dir / "selection.npy", idx_selection)

    # Save feature criteria
    for name, value in criteria.items():
        save_criteria(roi_processor.root_dir, name, value)
