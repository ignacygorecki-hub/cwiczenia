"""Overlay dose on CT slice and save/show.

Usage (simple):
  python scripts/overlay_dose_ct.py --ct examples/CT_small.dcm --dose examples/dose.npy --slice 0 --out examples/overlay_sample.png

If dose is DICOM RTDOSE the script applies DoseGridScaling.
"""
from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pydicom


def read_ct_slice(ct_path: Path, slice_index: int = 0) -> np.ndarray:
    ds = pydicom.dcmread(str(ct_path))
    arr = ds.pixel_array.astype(float)
    # if multi-slice, allow index
    if arr.ndim == 3:
        return arr[slice_index]
    return arr


def read_dose_slice(dose_path: Path, slice_index: int = 0) -> np.ndarray:
    if dose_path.suffix.lower() == '.npy':
        arr = np.load(dose_path)
    else:
        ds = pydicom.dcmread(str(dose_path))
        arr = ds.pixel_array.astype(float)
        scaling = getattr(ds, 'DoseGridScaling', None)
        if scaling is not None:
            arr = arr * float(scaling)
    if arr.ndim == 3:
        return arr[slice_index]
    return arr


def overlay_and_save(ct_slice: np.ndarray, dose_slice: np.ndarray, out_path: Path, alpha: float = 0.5, cmap: str = 'magma'):
    plt.figure(figsize=(6,6))
    plt.imshow(ct_slice, cmap='gray')
    plt.imshow(dose_slice, cmap=cmap, alpha=alpha)
    plt.axis('off')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--ct', required=True, help='Path to CT DICOM file')
    p.add_argument('--dose', required=True, help='Path to dose (npy or RTDOSE DICOM)')
    p.add_argument('--slice', type=int, default=0, help='Slice index')
    p.add_argument('--out', required=True, help='Output PNG path')
    args = p.parse_args(argv)

    ct = read_ct_slice(Path(args.ct), args.slice)
    dose = read_dose_slice(Path(args.dose), args.slice)
    overlay_and_save(ct, dose, Path(args.out))


if __name__ == '__main__':
    main()
