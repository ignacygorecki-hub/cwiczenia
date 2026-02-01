from scripts.read_dicom import read_and_print
from pydicom.data import get_testdata_file


def test_read_and_print_covers_basic_info(capsys):
    sample = get_testdata_file("CT_small.dcm")
    # Run the function and capture stdout
    read_and_print(sample, show_image=False)
    captured = capsys.readouterr()
    out = captured.out
    assert "Paczjent" not in out  # sanity check for language typo
    assert "Pacjent" in out
    assert "Modalność" in out or "Modality" in out
    assert "Using sample file" not in out  # since we passed a path explicitly
