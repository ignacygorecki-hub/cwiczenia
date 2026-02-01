import importlib

pkgs = ["pydicom", "numpy", "matplotlib", "SimpleITK", "monai", "torch"]
for p in pkgs:
    try:
        m = importlib.import_module(p)
        ver = getattr(m, "__version__", None)
        if not ver:
            getv = getattr(m, "GetVersion", None) or getattr(m, "Version", None)
            if callable(getv):
                ver = getv()
        print(f"{p}: {ver}")
    except Exception as e:
        print(f"{p}: import failed: {e}")
