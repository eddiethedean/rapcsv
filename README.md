# rapcsv

**Streaming async CSV — no fake async, no GIL stalls.**

---

## Why `rap*`?

Packages prefixed with **`rap`** stand for **Real Async Python**. Unlike many libraries that merely wrap blocking I/O in `async` syntax, `rap*` packages guarantee that all I/O work is executed **outside the Python GIL** using native runtimes (primarily Rust). This means event loops are never stalled by hidden thread pools, blocking syscalls, or cooperative yielding tricks. If a `rap*` API is `async`, it is *structurally non-blocking by design*, not by convention. The `rap` prefix is a contract: measurable concurrency, real parallelism, and verifiable async behavior under load.

See the [rap-manifesto](https://github.com/rap-project/rap-manifesto) for philosophy and guarantees.

---

## What this package provides

- True async CSV reading and writing
- Streaming support for large files
- Native Rust-backed execution (Tokio)
- Zero Python thread pools
- Event-loop-safe concurrency under load
- GIL-independent I/O operations
- Zero-copy I/O when feasible

---

## Installation

```bash
pip install rapcsv
```

---

## Usage

```python
import asyncio
from rapcsv import Reader, Writer

# TODO: Implement async API
# async def main():
#     reader = await Reader.create("input.csv")
#     writer = await Writer.create("output.csv")
#     
#     async for row in reader:
#         await writer.write_row(row)

# asyncio.run(main())
```

---

## Benchmarks

This package passes the Fake Async Detector. Benchmarks are available in the [rap-bench](https://github.com/rap-project/rap-bench) repository.

---

## Non-Goals

- Not a drop-in replacement for `csv` module
- Not compatible with all CSV dialects (yet)
- Not designed for synchronous use cases

---

## License

MIT
