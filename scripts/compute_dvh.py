"""Compute Dose-Volume Histogram (DVH) from dose + mask arrays or DICOM RTDOSE.

Usage (simple):
  python scripts/compute_dvh.py --dose dose.npy --mask mask.npy --out examples/dvh_sample.png

If dose is a DICOM RTDOSE, the script will apply DoseGridScaling if present.
"""
from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pydicom


def read_dose(path: Path) -> np.ndarray:
    if path.suffix.lower() in ['.npy']:
        return np.load(path)
    ds = pydicom.dcmread(str(path))
    arr = ds.pixel_array.astype(float)
    scaling = getattr(ds, 'DoseGridScaling', None)
    if scaling is not None:
        arr = arr * float(scaling)
    return arr


def compute_dvh(dose: np.ndarray, mask: np.ndarray, bins: int = 1000):
    # Extract dose values inside mask
    vals = dose[mask > 0].ravel()
    if vals.size == 0:
        return np.array([0.0]), np.array([0.0])
    hist, bin_edges = np.histogram(vals, bins=bins, range=(vals.min(), vals.max()))
    cumsum = np.cumsum(hist[::-1])[::-1]
    vol_frac = cumsum / cumsum[0]
    # plot vs bin_edges[:-1]
    return bin_edges[:-1], vol_frac


def plot_dvh(dose_bins, vol_frac, out_path: Path | None = None):
    plt.figure()
    plt.plot(dose_bins, vol_frac)
    plt.xlabel('Dose (Gy)')
    plt.ylabel('Volume fraction')
    plt.ylim(0,1)
    plt.grid(True)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, bbox_inches='tight')
    else:
        plt.show()
    plt.close()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--dose', required=True, help='Path to dose (npy or RTDOSE DICOM)')
    p.add_argument('--mask', required=True, help='Path to mask (npy)')
    p.add_argument('--out', required=False, help='Output PNG for DVH')
    args = p.parse_args(argv)

    dose = read_dose(Path(args.dose))
    mask = np.load(args.mask)
    bins, vol = compute_dvh(dose, mask)
    plot_dvh(bins, vol, Path(args.out) if args.out else None)


if __name__ == '__main__':
    main()
