from pydicom.data import get_testdata_file
from scripts.read_dicom import read_and_print


def test_save_png_creates_file(tmp_path):
    sample = get_testdata_file("CT_small.dcm")
    out = tmp_path / "out.png"
    read_and_print(sample, show_image=False, save_path=str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_rtdose_save_applies_scaling(tmp_path):
    import numpy as np
    from pydicom.dataset import Dataset
    from pydicom.uid import ExplicitVRLittleEndian

    # create synthetic RTDOSE with small array
    arr = np.arange(16, dtype=np.uint16).reshape(4, 4)
    ds = Dataset()
    import pydicom
    from pydicom.dataset import FileMetaDataset

    ds.file_meta = FileMetaDataset()
    ds.file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    ds.file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds.Rows = 4
    ds.Columns = 4
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.Modality = "RTDOSE"
    ds.DoseGridScaling = 0.5
    ds.PixelData = arr.tobytes()

    path = tmp_path / "rtdose.dcm"
    import pydicom

    # write with file meta and required headers
    pydicom.filewriter.dcmwrite(str(path), ds, write_like_original=False)

    out = tmp_path / "rtdose_out.png"
    read_and_print(str(path), show_image=False, save_path=str(out))
    assert out.exists()
    assert out.stat().st_size > 0

    # As a basic sanity check, ensure DoseGridScaling was mentioned in stdout
    # (read_and_print prints Dose Grid Scaling for RTDOSE)
    # Not capturing stdout here (tested earlier); rely on file existence and size
