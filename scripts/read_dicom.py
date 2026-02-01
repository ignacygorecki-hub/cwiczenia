import argparse
import os
import numpy as np
import pydicom
from pydicom.data import get_testdata_file

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def _save_image(
    arr: np.ndarray, out_path: str, cmap: str = "gray", add_colorbar: bool = False
):
    """Save a numpy array as PNG using matplotlib."""
    if plt is None:
        raise RuntimeError("matplotlib is required to save images")
    fig, ax = plt.subplots()
    im = ax.imshow(arr, cmap=cmap)
    ax.axis("off")
    if add_colorbar:
        fig.colorbar(im, ax=ax)
    fig.tight_layout(pad=0)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


def read_and_print(path=None, show_image=False, save_path: str | None = None):
    """Read a DICOM file and print basic patient and technical info.

    If path is None, a pydicom sample file is used. If show_image is True the
    image will be displayed (requires matplotlib). If save_path is provided
    the pixel data will be saved as PNG to that path.
    """
    if path is None:
        path = get_testdata_file("CT_small.dcm")
        print(f"Using sample file: {path}")

    ds = pydicom.dcmread(path)

    def safe(attr):
        return getattr(ds, attr, "<brak>")

    print("--- PODSTAWOWE DANE PACJENTA ---")
    print(f"Pacjent: {safe('PatientName')}")
    print(f"ID: {safe('PatientID')}")
    print(f"Płeć: {safe('PatientSex')}")
    print(f"Data badania: {safe('ContentDate') or safe('StudyDate')}")

    print("\n--- PARAMETRY TECHNICZNE ---")
    modality = safe("Modality")
    print(f"Modalność: {modality}")
    print(f"Producent: {safe('Manufacturer')}")
    print(f"Slice Thickness: {safe('SliceThickness')}")

    is_rtdose = modality == "RTDOSE"
    if is_rtdose:
        print(f"Jednostka dawki: {safe('DoseUnits')}")
        print(f"Dose Grid Scaling: {safe('DoseGridScaling')}")

    # Handle image display and saving
    if "PixelData" in ds:
        arr = ds.pixel_array.astype(float)

        if is_rtdose:
            # Apply DoseGridScaling if available
            scaling = getattr(ds, "DoseGridScaling", None)
            if scaling is not None:
                try:
                    arr = arr * float(scaling)
                except Exception:
                    print("Warning: could not apply DoseGridScaling (invalid value)")
            cmap = "magma"
            add_colorbar = True
        else:
            cmap = "gray"
            add_colorbar = False

        if save_path:
            # Ensure directory exists
            out_dir = os.path.dirname(save_path) or "."
            os.makedirs(out_dir, exist_ok=True)
            try:
                _save_image(arr, save_path, cmap=cmap, add_colorbar=add_colorbar)
                print(f"Saved image to: {save_path}")
            except Exception as e:
                print(f"Failed to save image: {e}")

        if show_image:
            if plt is None:
                print("matplotlib is not available; cannot show image")
            else:
                plt.imshow(arr, cmap=cmap)
                plt.title(f"{modality} image")
                if add_colorbar:
                    plt.colorbar()
                plt.axis("off")
                plt.show()


def _build_default_save_path(path: str, suffix: str = ".png") -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    return f"{base}{suffix}"


def main(argv: list | None = None):
    parser = argparse.ArgumentParser(
        description="Read DICOM and show/save basic info and image"
    )
    parser.add_argument(
        "path", nargs="?", help="Path to DICOM file (uses pydicom sample if omitted)"
    )
    parser.add_argument(
        "--show", action="store_true", help="Show the image (requires matplotlib)"
    )
    parser.add_argument(
        "--save",
        nargs="?",
        const="",
        help="Save pixel data to PNG. Optionally provide output path",
    )
    args = parser.parse_args(argv)

    save_path = None
    if args.save is not None:
        if args.save == "":
            if args.path:
                save_path = _build_default_save_path(args.path)
            else:
                # when no path is given, use sample filename
                sample = get_testdata_file("CT_small.dcm")
                save_path = _build_default_save_path(sample)
        else:
            save_path = args.save

    read_and_print(args.path, show_image=args.show, save_path=save_path)


if __name__ == "__main__":
    main()
