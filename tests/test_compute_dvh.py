import numpy as np
from scripts.compute_dvh import compute_dvh, plot_dvh



def test_compute_dvh_basic(tmp_path):
    dose = np.linspace(0, 100, 1000).reshape((10, 10, 10))
    mask = np.zeros_like(dose)
    mask[2:8, 2:8, 2:8] = 1
    bins, vol = compute_dvh(dose, mask, bins=50)
    assert len(bins) == 50
    assert vol[0] == 1.0
    # export a plot
    out = tmp_path / "dvh.png"
    plot_dvh(bins, vol, out)
    assert out.exists() and out.stat().st_size > 0
