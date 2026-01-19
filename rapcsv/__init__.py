"""Streaming async CSV — no fake async, no GIL stalls.

rapcsv provides true async CSV reading and writing for Python, backed by Rust and Tokio.
Unlike libraries that wrap blocking I/O in async syntax, rapcsv guarantees that all CSV
operations execute **outside the Python GIL**, ensuring event loops never stall under load.

Features:
    - True async CSV reading and writing
    - Streaming support for large files (incremental reading, no full file load)
    - Context manager support (`async with`)
    - aiocsv compatibility (AsyncReader/AsyncWriter aliases)
    - CSV-specific exception types (CSVError, CSVFieldCountError)
    - RFC 4180 compliant CSV parsing and writing

Example:
    >>> import asyncio
    >>> from rapcsv import Reader, Writer
    >>>
    >>> async def main():
    ...     async with Writer("output.csv") as writer:
    ...         await writer.write_row(["name", "age"])
    ...         await writer.write_row(["Alice", "30"])
    ...
    ...     async with Reader("output.csv") as reader:
    ...         row = await reader.read_row()
    ...         print(row)  # ['name', 'age']
    >>>
    >>> asyncio.run(main())

For more information, see: https://github.com/eddiethedean/rapcsv
"""

from typing import List, Protocol, runtime_checkable

@runtime_checkable
class WithAsyncRead(Protocol):
    """Protocol for async file-like objects with read method."""
    async def read(self, size: int) -> str:
        """Read up to size bytes/characters from the file."""
        ...

@runtime_checkable
class WithAsyncWrite(Protocol):
    """Protocol for async file-like objects with write method."""
    async def write(self, data: str) -> None:
        """Write data to the file."""
        ...

# Internal helper function to call async file methods from any thread
# This schedules the call on the event loop using run_coroutine_threadsafe
def _call_file_method_threadsafe(file_handle, method_name, event_loop, *args):
    """Call an async file method from any thread by scheduling it on the event loop.
    
    This is used by the Rust extension to call rapfiles methods from spawn_blocking threads.
    
    Args:
        file_handle: The file handle object
        method_name: Name of the method to call (e.g., "write", "read")
        event_loop: The event loop to schedule the call on
        *args: Arguments to pass to the method
    """
    import asyncio
    
    # Create a coroutine that calls the method
    async def _call_method():
        method = getattr(file_handle, method_name)
        result = method(*args)
        # If it returns a Future or coroutine, await it
        if hasattr(result, '__await__'):
            return await result
        return result
    
    # Schedule the coroutine on the event loop
    # This will execute on the event loop thread, not the current thread
    future = asyncio.run_coroutine_threadsafe(_call_method(), event_loop)
    return future.result()

# Internal helper function to wrap Futures into coroutines for run_coroutine_threadsafe
# This is used by the Rust extension to convert rapfiles Futures to coroutines
def _await_wrapper(fut):
    """Wrap a Future into a coroutine using types.coroutine.
    
    This function is called from Rust code to convert asyncio.Future objects
    (like those returned by rapfiles) into coroutines that can be used with
    asyncio.run_coroutine_threadsafe().
    
    This function must work even when called from a thread without an event loop.
    """
    import types
    import inspect
    
    # Check if already a coroutine using inspect (doesn't need event loop)
    if inspect.iscoroutine(fut):
        return fut
    
    # It's a Future - wrap it in a generator function, then use types.coroutine
    # This approach doesn't require an event loop to be running
    # The generator will be executed on the event loop via run_coroutine_threadsafe
    def _gen_wrapper(fut):
        # yield from will work when the coroutine is executed on the event loop
        # This doesn't execute immediately - it just creates a generator
        return (yield from fut)
    
    # Wrap the generator function with types.coroutine to make it a coroutine function
    coro_func = types.coroutine(_gen_wrapper)
    
    # Call it to get a coroutine object (doesn't execute yet, no event loop needed)
    # The coroutine will be executed later on the event loop
    return coro_func(fut)

try:
    from _rapcsv import Reader, Writer, AsyncDictReader, AsyncDictWriter, CSVError, CSVFieldCountError  # type: ignore[import-not-found]
except ImportError:
    try:
        from rapcsv._rapcsv import Reader, Writer, AsyncDictReader, AsyncDictWriter, CSVError, CSVFieldCountError
    except ImportError:
        raise ImportError(
            "Could not import _rapcsv. Make sure rapcsv is built with maturin."
        )

# API compatibility with aiocsv
# aiocsv uses AsyncReader and AsyncWriter as class names
AsyncReader = Reader
AsyncWriter = Writer

__version__: str = "0.1.2"
__all__: List[str] = [
    "Reader",
    "Writer",
    "AsyncDictReader",
    "AsyncDictWriter",
    "AsyncReader",  # aiocsv compatibility
    "AsyncWriter",  # aiocsv compatibility
    "CSVError",
    "CSVFieldCountError",
    "WithAsyncRead",  # Protocol for type checking
    "WithAsyncWrite",  # Protocol for type checking
]
