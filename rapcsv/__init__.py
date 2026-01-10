"""Streaming async CSV — no fake async, no GIL stalls."""

try:
    from _rapcsv import Reader, Writer
except ImportError:
    try:
        from rapcsv._rapcsv import Reader, Writer
    except ImportError:
        raise ImportError("Could not import _rapcsv. Make sure rapcsv is built with maturin.")

__version__ = "0.0.1"
__all__ = ["Reader", "Writer"]

