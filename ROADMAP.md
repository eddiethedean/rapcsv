# rapcsv Roadmap

This roadmap outlines the development plan for `rapcsv`, aligned with the [RAP Project Strategic Plan](../rap-project-plan.md). `rapcsv` provides true async CSV reading and writing for Python, backed by Rust and Tokio.

## Current Status

**MVP Version (v0.0.1)** - Current limitations:

- Reader reads from the start of the file each time (reads entire file on each call)
- Writer requires separate instances for multiple rows (opens/closes file on each write)
- Simple CSV implementation (no proper escaping, quoting, or dialect support)
- No streaming support for large files
- Limited error handling
- No header detection or manipulation
- Not yet a drop-in replacement for `aiocsv`

**Goal**: Achieve drop-in replacement compatibility with `aiocsv` to enable seamless migration with true async performance.

## Phase 1 — Credibility

Focus: Remove MVP limitations and establish stable, production-ready core functionality.

### Core Improvements

- **Fix Reader position tracking**
  - Implement proper file cursor management
  - Stream file reading instead of reading entire file on each call
  - Maintain position state across `read_row()` calls
  - Efficient buffering with BufReader

- **Enable Writer to write multiple rows**
  - Maintain file handle across multiple `write_row()` calls
  - Support append mode properly
  - Add `close()` or context manager support
  - Proper file handle lifecycle management

- **Proper CSV escaping and quoting**
  - Implement RFC 4180 compliant CSV writing
  - Handle special characters (commas, quotes, newlines)
  - Support quoted fields and escaped quotes
  - Proper CSV parsing with quoted field handling

- **Improved error handling**
  - Better error messages with context
  - Proper exception types (CSV-specific errors)
  - Handle malformed CSV gracefully
  - File I/O error differentiation

- **API stability improvements**
  - Context manager support (`async with`)
  - Connection state management
  - Resource cleanup guarantees

- **Performance optimizations**
  - Reduce file I/O overhead
  - Efficient buffering strategies
  - Memory usage improvements

### API Compatibility for Drop-In Replacement

- **aiocsv API compatibility**
  - Match `aiocsv.AsyncReader` and `aiocsv.AsyncWriter` APIs
  - Compatible function signatures and method names
  - Matching exception types and error behavior
  - Compatible context manager behavior
  - Drop-in replacement validation: `import rapcsv as aiocsv` compatibility tests

- **Migration support**
  - Compatibility shim/adapter layer if needed for exact API matching
  - Migration guide documenting any differences
  - Backward compatibility considerations

### Testing & Validation

- Comprehensive test suite covering edge cases
- Fake Async Detector validation passes under load
- **Pass 100% of aiocsv test suite** as drop-in replacement validation
- Drop-in replacement compatibility tests (can swap `aiocsv` → `rapcsv` without code changes)
- Benchmark comparison with existing CSV libraries
- Documentation improvements including migration guide

## Phase 2 — Expansion

Focus: Feature additions, performance enhancements, and broader compatibility.

### Streaming Support

- **True streaming for large files**
  - Stream-based reading without loading entire file
  - Chunked processing for memory efficiency
  - Support for files larger than available memory
  - Iterator-style API (`async for` support)

- **Streaming Writer**
  - Buffered writing with configurable buffer sizes
  - Flush control for real-time updates
  - Memory-efficient batch writing

### CSV Dialect Support

- **Multiple CSV dialects**
  - Custom delimiters (not just comma)
  - Custom quote characters
  - Custom line terminators (CRLF, LF, CR)
  - Excel, Unix, RFC 4180 dialects
  - Dialect detection and configuration

- **Header handling**
  - Automatic header detection
  - Header row skipping
  - Named field access (dictionary-style rows)
  - Header manipulation (add, remove, rename)

### Advanced Features

- **Reader enhancements**
  - `read_rows(n)` - read multiple rows at once
  - `skip_rows(n)` - skip rows efficiently
  - Row filtering and transformation
  - Progress tracking for large files

- **Writer enhancements**
  - `write_rows()` - write multiple rows efficiently
  - Header row writing
  - Automatic field ordering
  - Column validation

- **Type conversion**
  - Automatic type inference
  - Configurable type converters
  - Date/time parsing
  - Numeric type handling

### Performance & Compatibility

- **Performance benchmarks**
  - Comparison with `csv`, `aiofiles`, `pandas`
  - Throughput and latency metrics
  - Memory usage profiles
  - Concurrent operation benchmarks

- **Additional API compatibility**
  - Maintain and refine aiocsv drop-in replacement (achieved in Phase 1)
  - Optional compatibility layer with Python's standard `csv` module API
  - Migration guides for existing code from aiocsv and csv module
  - Backwards compatibility maintenance across versions

## Phase 3 — Ecosystem

Focus: Advanced features, ecosystem integration, and zero-copy optimizations.

### Zero-Copy Streaming

- **Efficient data transfer**
  - Zero-copy operations where possible
  - Memory-mapped file support for large files
  - Direct buffer passing to reduce allocations
  - SIMD-accelerated CSV parsing (where applicable)

### Advanced Parsing Options

- **Flexible parsing**
  - Custom field parsers
  - Validation rules and schemas
  - Error recovery strategies
  - Partial parsing support

- **Schema support**
  - CSV schema definitions
  - Type validation per column
  - Required/optional field support
  - Default value handling

### Integration & Ecosystem

- **rap-core integration**
  - Shared primitives with other rap packages
  - Common I/O patterns
  - Unified error handling
  - Performance monitoring hooks

- **Framework compatibility**
  - Integration examples with FastAPI, aiohttp
  - Data pipeline patterns
  - ETL workflow support
  - Database import/export utilities

### Advanced Features

- **Parallel processing**
  - Multi-file processing
  - Chunk-based parallel parsing
  - Concurrent read/write operations
  - Distributed processing patterns

- **Monitoring & Observability**
  - Performance metrics export
  - Progress callbacks
  - Resource usage tracking
  - Debugging tools

### Documentation & Community

- **Comprehensive documentation**
  - Advanced usage patterns
  - Performance tuning guides
  - Migration documentation
  - Contributing guidelines

- **Ecosystem presence**
  - PyPI package optimization
  - CI/CD pipeline improvements
  - Community examples and tutorials
  - Blog posts and case studies

## Cross-Package Dependencies

- **Phase 1**: Independent development, minimal dependencies
- **Phase 2**: Potential integration with `rapfiles` for advanced file operations
- **Phase 3**: Integration with `rap-core` for shared primitives and `rapsqlite` for database import/export patterns

## Success Criteria

- **Phase 1**: Removed all MVP limitations, stable API, **drop-in replacement for aiocsv**, passes 100% of aiocsv test suite, passes Fake Async Detector under all load conditions
- **Phase 2**: Feature-complete for common CSV use cases, competitive performance benchmarks, good documentation, seamless migration from aiocsv
- **Phase 3**: Industry-leading performance, ecosystem integration, adoption in production systems as preferred aiocsv alternative

## Versioning Strategy

Following semantic versioning:
- `v0.x`: Breaking changes allowed, MVP and Phase 1 development
- `v1.0`: Stable API, Phase 1 complete, production-ready
- `v1.x+`: Phase 2 and 3 features, backwards-compatible additions

