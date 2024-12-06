from importlib.metadata import PackageNotFoundError, version

try:
    DIST_NAME = "iqm-pypitest"
    __version__ = version(DIST_NAME)
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
