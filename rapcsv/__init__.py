"""Streaming async CSV — no fake async, no GIL stalls."""

from rapcsv._rapcsv import Reader, Writer

__version__ = "0.0.1"
__all__ = ["Reader", "Writer"]

