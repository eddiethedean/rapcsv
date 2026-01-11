"""Streaming async CSV — no fake async, no GIL stalls."""

from typing import List

try:
    from _rapcsv import Reader, Writer  # type: ignore[import-not-found]
except ImportError:
    try:
        from rapcsv._rapcsv import Reader, Writer
    except ImportError:
        raise ImportError(
            "Could not import _rapcsv. Make sure rapcsv is built with maturin."
        )

__version__: str = "0.0.2"
__all__: List[str] = ["Reader", "Writer"]
