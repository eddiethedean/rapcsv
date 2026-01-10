# rapcsv

**Streaming async CSV — no fake async, no GIL stalls.**

[![PyPI version](https://badge.fury.io/py/rapcsv.svg)](https://badge.fury.io/py/rapcsv)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`rapcsv` provides true async CSV reading and writing for Python, backed by Rust and Tokio. Unlike libraries that wrap blocking I/O in `async` syntax, `rapcsv` guarantees that all CSV operations execute **outside the Python GIL**, ensuring event loops never stall under load, even when processing large files.

**Roadmap Goal**: Achieve drop-in replacement compatibility with `aiocsv`, enabling seamless migration with true async performance. See [ROADMAP.md](https://github.com/eddiethedean/rapcsv/blob/main/ROADMAP.md) for details.

## Why `rap*`?

Packages prefixed with **`rap`** stand for **Real Async Python**. Unlike many libraries that merely wrap blocking I/O in `async` syntax, `rap*` packages guarantee that all I/O work is executed **outside the Python GIL** using native runtimes (primarily Rust). This means event loops are never stalled by hidden thread pools, blocking syscalls, or cooperative yielding tricks. If a `rap*` API is `async`, it is *structurally non-blocking by design*, not by convention. The `rap` prefix is a contract: measurable concurrency, real parallelism, and verifiable async behavior under load.

See the [rap-manifesto](https://github.com/eddiethedean/rap-manifesto) for philosophy and guarantees.

## Features

- ✅ **True async** CSV reading and writing
- ✅ **Streaming support** for large files
- ✅ **Native Rust-backed** execution (Tokio)
- ✅ **Zero Python thread pools**
- ✅ **Event-loop-safe** concurrency under load
- ✅ **GIL-independent** I/O operations
- ✅ **Verified** by Fake Async Detector

## Requirements

- Python 3.8+
- Rust 1.70+ (for building from source)

## Installation

```bash
pip install rapcsv
```

### Building from Source

```bash
git clone https://github.com/eddiethedean/rapcsv.git
cd rapcsv
pip install maturin
maturin develop
```

---

## Usage

```python
import asyncio
from rapcsv import Reader, Writer

async def main():
    # Write CSV file (one row per Writer instance for MVP)
    writer = Writer("output.csv")
    await writer.write_row(["name", "age", "city"])
    
    # Read CSV file (reads first row)
    reader = Reader("output.csv")
    row = await reader.read_row()
    print(row)  # Output: ['name', 'age', 'city']

asyncio.run(main())
```

### Writing Multiple Rows

```python
import asyncio
from rapcsv import Writer

async def main():
    # Write each row with a new Writer instance (MVP limitation)
    rows = [
        ["name", "age", "city"],
        ["Alice", "30", "New York"],
        ["Bob", "25", "London"],
    ]
    
    for row in rows:
        writer = Writer("output.csv")
        await writer.write_row(row)
    
    # Verify file contents
    with open("output.csv") as f:
        print(f.read())

asyncio.run(main())
```

**Note**: In the MVP version, each `write_row` call opens and closes the file. For multiple rows, use separate `Writer` instances. The Reader reads one row at a time from the start of the file (MVP limitation).

## API Reference

### `Reader(path: str)`

Create a new async CSV reader.

**Parameters:**
- `path` (str): Path to the CSV file to read

**Example:**
```python
reader = Reader("data.csv")
```

### `Reader.read_row() -> List[str]`

Read the next row from the CSV file.

**Returns:**
- `List[str]`: A list of string values for the row, or an empty list if EOF

**Raises:**
- `IOError`: If the file cannot be read or parsed

**Note**: In MVP version, reads from the start of the file each time.

### `Writer(path: str)`

Create a new async CSV writer.

**Parameters:**
- `path` (str): Path to the CSV file to write

**Example:**
```python
writer = Writer("output.csv")
```

### `Writer.write_row(row: List[str]) -> None`

Write a row to the CSV file.

**Parameters:**
- `row` (List[str]): A list of string values to write as a CSV row

**Raises:**
- `IOError`: If the file cannot be written

**Note**: In MVP version, each `write_row` call opens and closes the file. Use separate `Writer` instances for multiple rows.

## Benchmarks

This package passes the [Fake Async Detector](https://github.com/eddiethedean/rap-bench). Benchmarks are available in the [rap-bench](https://github.com/eddiethedean/rap-bench) repository.

Run the detector yourself:

```bash
pip install rap-bench
rap-bench detect rapcsv
```

## Roadmap

See [ROADMAP.md](https://github.com/eddiethedean/rapcsv/blob/main/ROADMAP.md) for detailed development plans. Key goals include:
- Drop-in replacement for `aiocsv` (Phase 1)
- Full streaming support for large files
- Comprehensive CSV dialect support
- Zero-copy optimizations

## Related Projects

- [rap-manifesto](https://github.com/eddiethedean/rap-manifesto) - Philosophy and guarantees
- [rap-bench](https://github.com/eddiethedean/rap-bench) - Fake Async Detector CLI
- [rapfiles](https://github.com/eddiethedean/rapfiles) - True async filesystem I/O
- [rapsqlite](https://github.com/eddiethedean/rapsqlite) - True async SQLite

## Limitations (MVP v0.0.1)

**Current MVP limitations:**
- Reader reads from start each time (reads entire file on each call)
- Writer requires separate instances for multiple rows (opens/closes file on each call)
- Simple CSV implementation (no proper escaping, quoting, or dialect support)
- Not yet a drop-in replacement for `aiocsv` (goal for Phase 1)
- Not designed for synchronous use cases

**Roadmap**: See [ROADMAP.md](https://github.com/eddiethedean/rapcsv/blob/main/ROADMAP.md) for planned improvements. Our goal is to achieve drop-in replacement compatibility with `aiocsv` while providing true async performance with GIL-independent I/O.

## Contributing

Contributions are welcome! Please see our [contributing guidelines](https://github.com/eddiethedean/rapcsv/blob/main/CONTRIBUTING.md) (coming soon).

## License

MIT

## Changelog

See [CHANGELOG.md](https://github.com/eddiethedean/rapcsv/blob/main/CHANGELOG.md) (coming soon) for version history.
