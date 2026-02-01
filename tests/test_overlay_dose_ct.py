import numpy as np
from scripts.overlay_dose_ct import overlay_and_save


def test_overlay_and_save(tmp_path):
    ct = np.tile(np.linspace(0,255,64),(64,1)).astype(float)
    dose = np.zeros_like(ct)
    dose[20:44,20:44] = 50
    out = tmp_path / 'overlay.png'
    overlay_and_save(ct, dose, out)
    assert out.exists() and out.stat().st_size > 0
