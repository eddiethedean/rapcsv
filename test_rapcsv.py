"""Test rapcsv async functionality."""

import pytest
import tempfile
import os

from rapcsv import Reader, Writer


@pytest.mark.asyncio
async def test_write_row():
    """Test writing a CSV row."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name

    try:
        writer = Writer(test_file)
        await writer.write_row(["col1", "col2", "col3"])

        # Verify file was written
        assert os.path.exists(test_file), "CSV file should exist"

        # Verify content
        with open(test_file, "r") as f:
            content = f.read()
        assert "col1" in content
        assert "col2" in content
        assert "col3" in content
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


@pytest.mark.asyncio
async def test_write_multiple_rows():
    """Test writing multiple CSV rows."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name

    try:
        writer = Writer(test_file)
        await writer.write_row(["name", "age", "city"])
        await writer.write_row(["Alice", "30", "New York"])
        await writer.write_row(["Bob", "25", "London"])

        # Verify content
        with open(test_file, "r") as f:
            lines = f.readlines()
        assert len(lines) >= 3, "Should have at least 3 rows"
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


@pytest.mark.asyncio
async def test_read_row():
    """Test reading a CSV row."""
    # Create CSV file first
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name
        f.write("col1,col2,col3\n")
        f.write("val1,val2,val3\n")

    try:
        reader = Reader(test_file)
        row = await reader.read_row()
        assert len(row) == 3, f"Expected 3 columns, got {len(row)}"
        assert row == ["col1", "col2", "col3"], (
            f"Expected ['col1', 'col2', 'col3'], got {row}"
        )
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


@pytest.mark.asyncio
async def test_read_multiple_rows():
    """Test reading multiple CSV rows sequentially."""
    # Create CSV file first
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name
        f.write("col1,col2\n")
        f.write("val1,val2\n")
        f.write("val3,val4\n")

    try:
        reader = Reader(test_file)
        row1 = await reader.read_row()
        assert row1 == ["col1", "col2"], f"Expected ['col1', 'col2'], got {row1}"

        row2 = await reader.read_row()
        assert row2 == ["val1", "val2"], f"Expected ['val1', 'val2'], got {row2}"

        row3 = await reader.read_row()
        assert row3 == ["val3", "val4"], f"Expected ['val3', 'val4'], got {row3}"
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


@pytest.mark.asyncio
async def test_write_read_roundtrip():
    """Test writing and reading CSV in sequence."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name

    try:
        # Write rows
        writer = Writer(test_file)
        await writer.write_row(["name", "age"])
        await writer.write_row(["Alice", "30"])

        # Read rows
        reader = Reader(test_file)
        header = await reader.read_row()
        assert header == ["name", "age"], f"Expected ['name', 'age'], got {header}"

        row = await reader.read_row()
        assert row == ["Alice", "30"], f"Expected ['Alice', '30'], got {row}"
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


@pytest.mark.asyncio
async def test_csv_escaping():
    """Test that CSV special characters are properly escaped."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        test_file = f.name

    try:
        writer = Writer(test_file)
        # Test comma, quote, and newline in data
        await writer.write_row(
            ["value,with,commas", 'value"with"quotes', "value\nwith\nnewlines"]
        )

        reader = Reader(test_file)
        row = await reader.read_row()
        assert len(row) == 3, f"Expected 3 columns, got {len(row)}"
        assert "value,with,commas" in row[0] or "value,with,commas" == row[0]
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)
