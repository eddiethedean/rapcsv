"""Type stubs for _rapcsv Rust extension module."""

from typing import Coroutine, Any, List, Optional, Dict

class Reader:
    def __init__(
        self,
        path: str,
        delimiter: Optional[str] = None,
        quotechar: Optional[str] = None,
        escapechar: Optional[str] = None,
        quoting: Optional[int] = None,
        lineterminator: Optional[str] = None,
        skipinitialspace: Optional[bool] = None,
        strict: Optional[bool] = None,
        double_quote: Optional[bool] = None,
        read_size: Optional[int] = None,
        field_size_limit: Optional[int] = None,
    ) -> None: ...
    def read_row(self) -> Coroutine[Any, Any, List[str]]: ...
    def read_rows(self, n: int) -> Coroutine[Any, Any, List[List[str]]]: ...
    def skip_rows(self, n: int) -> Coroutine[Any, Any, None]: ...
    @property
    def line_num(self) -> int: ...
    def __aiter__(self) -> "Reader": ...
    def __anext__(self) -> Coroutine[Any, Any, List[str]]: ...
    def __aenter__(self) -> Coroutine[Any, Any, "Reader"]: ...
    def __aexit__(
        self,
        exc_type: Optional[Any],
        exc_val: Optional[Any],
        exc_tb: Optional[Any],
    ) -> Coroutine[Any, Any, None]: ...

class Writer:
    def __init__(
        self,
        path: str,
        delimiter: Optional[str] = None,
        quotechar: Optional[str] = None,
        escapechar: Optional[str] = None,
        quoting: Optional[int] = None,
        lineterminator: Optional[str] = None,
        double_quote: Optional[bool] = None,
    ) -> None: ...
    def write_row(self, row: List[str]) -> Coroutine[Any, Any, None]: ...
    def writerows(self, rows: List[List[str]]) -> Coroutine[Any, Any, None]: ...
    def close(self) -> Coroutine[Any, Any, None]: ...
    def __aenter__(self) -> Coroutine[Any, Any, "Writer"]: ...
    def __aexit__(
        self,
        exc_type: Optional[Any],
        exc_val: Optional[Any],
        exc_tb: Optional[Any],
    ) -> Coroutine[Any, Any, None]: ...

class AsyncDictReader:
    def __init__(
        self,
        path: str,
        fieldnames: Optional[List[str]] = None,
        restkey: Optional[str] = None,
        restval: Optional[str] = None,
        delimiter: Optional[str] = None,
        quotechar: Optional[str] = None,
        escapechar: Optional[str] = None,
        quoting: Optional[int] = None,
        lineterminator: Optional[str] = None,
        skipinitialspace: Optional[bool] = None,
        strict: Optional[bool] = None,
        double_quote: Optional[bool] = None,
        read_size: Optional[int] = None,
    ) -> None: ...
    def read_row(self) -> Coroutine[Any, Any, Dict[str, str]]: ...
    def get_fieldnames(self) -> Coroutine[Any, Any, Optional[List[str]]]: ...
    @property
    def fieldnames(self) -> Optional[List[str]]: ...

class AsyncDictWriter:
    def __init__(
        self,
        path: str,
        fieldnames: List[str],
        extrasaction: str = "raise",
        restval: str = "",
        delimiter: Optional[str] = None,
        quotechar: Optional[str] = None,
        escapechar: Optional[str] = None,
        quoting: Optional[int] = None,
        lineterminator: Optional[str] = None,
        skipinitialspace: Optional[bool] = None,
        strict: Optional[bool] = None,
        double_quote: Optional[bool] = None,
        write_size: Optional[int] = None,
    ) -> None: ...
    def writeheader(self) -> Coroutine[Any, Any, None]: ...
    def writerow(self, dict_row: Dict[str, str]) -> Coroutine[Any, Any, None]: ...
    def writerows(self, dict_rows: List[Dict[str, str]]) -> Coroutine[Any, Any, None]: ...

class CSVError(Exception):
    def __init__(self, message: str) -> None: ...

class CSVFieldCountError(Exception):
    def __init__(self, message: str) -> None: ...