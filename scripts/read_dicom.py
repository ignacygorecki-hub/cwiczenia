import sys
import pydicom
from pydicom.data import get_testdata_file

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def read_and_print(path=None, show_image=False):
    """Read a DICOM file and print basic patient and technical info.

    If path is None, a pydicom sample file is used.
    If show_image is True and the file contains PixelData and matplotlib is available,
    the image will be displayed.
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
    print(f"Modalność: {safe('Modality')}")
    print(f"Producent: {safe('Manufacturer')}")
    print(f"Slice Thickness: {safe('SliceThickness')}")

    if safe("Modality") == "RTDOSE":
        print(f"Jednostka dawki: {safe('DoseUnits')}")
        print(f"Dose Grid Scaling: {safe('DoseGridScaling')}")

    if show_image and "PixelData" in ds:
        if plt is None:
            print("matplotlib is not available; cannot show image")
            return
        arr = ds.pixel_array
        plt.imshow(arr, cmap="gray")
        plt.title(f"{safe('Modality')} image")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    # Avoid showing image in automated runs by default
    read_and_print(path_arg, show_image=False)
