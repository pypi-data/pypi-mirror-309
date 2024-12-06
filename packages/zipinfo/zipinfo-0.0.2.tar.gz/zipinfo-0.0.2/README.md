# ZipInfo Utility

`ZipInfo` is a Python utility for analyzing and parsing ZIP file structures, specifically the End of Central Directory (EOCD) and Central Directory Record (CDR) sections. This tool helps to locate and extract information about files within ZIP archives by identifying critical offsets, directory structures, and file metadata.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
- [Logging](#logging)
- [Example](#example)
- [License](#license)

---

## Installation

Since this utility does not require any external libraries beyond Python's standard library, you can simply include `ZipInfo` in your project.

## Usage

The `ZipInfo` class provides methods for:
- Calculating offsets in a ZIP file.
- Identifying the location of the Central Directory in a ZIP file.
- Parsing and extracting metadata for each file in the Central Directory.

### Methods

#### `ZipInfo.get_offset(offset: int) -> int`
- **Description**: Computes the offset within a file, normalized to megabytes.
- **Parameters**:
  - `offset` (int): The offset in bytes.
- **Returns**: An integer representing the normalized offset.

#### `ZipInfo.find_central_directory(data: bytes) -> tuple`
- **Description**: Searches for the End of Central Directory (EOCD) in the provided data.
- **Parameters**:
  - `data` (bytes): The byte sequence of the ZIP file.
- **Returns**: A tuple containing:
  - `central_dir_offset`: Offset of the Central Directory in the ZIP file.
  - `central_dir_size`: Size of the Central Directory.
  - `total_entries`: Number of entries in the Central Directory.

#### `ZipInfo.parse_eocd(eocd_data: bytes) -> tuple`
- **Description**: Parses the EOCD data to retrieve important directory metadata.
- **Parameters**:
  - `eocd_data` (bytes): The EOCD record data.
- **Returns**: A tuple with details including:
  - `central_dir_offset`: Offset of the Central Directory.
  - `central_dir_size`: Size of the Central Directory.
  - `total_entries`: Number of entries in the Central Directory.

#### `ZipInfo.parse_central_directory(data: bytes, data_offset: int, total_records: int) -> list`
- **Description**: Parses the Central Directory and extracts metadata for each file entry.
- **Parameters**:
  - `data` (bytes): The byte sequence of the ZIP file.
  - `data_offset` (int): Offset where the Central Directory begins.
  - `total_records` (int): Total number of file records in the Central Directory.
- **Returns**: A list of dictionaries, each containing:
  - `filename`: Name of the file.
  - `start_byte`: Start byte offset of the file's local header.
  - `end_byte`: End byte offset of the file's data.

## Logging

The `ZipInfo` class includes logging via Python’s `logging` library to provide insights into various stages of parsing. Enable `DEBUG` level logging to see detailed information, such as finding the EOCD and CDR signatures and handling unexpected records.

Example setup:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Example

```python
from zip import ZipInfo  # Import the ZipInfo class

# Load your ZIP file data as bytes
with open("example.zip", "rb") as f:
    data = f.read()

# Locate the Central Directory
central_dir_offset, central_dir_size, total_entries = ZipInfo.find_central_directory(data)

if central_dir_offset is not None:
    # Parse the Central Directory for file information
    file_info = ZipInfo.parse_central_directory(data, central_dir_offset, total_entries)
    print(file_info)  # List of dictionaries with file metadata
else:
    print("Central Directory not found.")
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/r0uted/zipinfo/blob/main/LICENSE) file for details.

---