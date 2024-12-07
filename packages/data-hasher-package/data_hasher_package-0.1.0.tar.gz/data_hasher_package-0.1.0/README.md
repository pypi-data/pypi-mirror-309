
# Data Hasher Package

This package provides a `DataHasher` class to generate and verify MD5 hashes of files.

## Installation
To install the package, use:
```bash
pip install .
```

## Usage
```python
from data_hasher import DataHasher

# Example usage
hasher = DataHasher()

# Hash a file
file_hash = hasher.create_hash("/path/to/file.txt")
print(f"MD5 Hash: {file_hash}")

# Verify file hash
is_valid = hasher.verify_file_hash("/path/to/data_5d41402abc4b2a76b9719d911017c592.txt")
print(f"Is file valid: {is_valid}")

# Hash a DataFrame
import pandas as pd
df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
df_hash = hasher.create_hash_from_dataframe(df)
print(f"DataFrame MD5 Hash: {df_hash}")
```
