"""Connected Models: a small deterministic composition core."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("connected-models")
except PackageNotFoundError:  # pragma: no cover - running from source without install
    __version__ = "0.0.0+unknown"
