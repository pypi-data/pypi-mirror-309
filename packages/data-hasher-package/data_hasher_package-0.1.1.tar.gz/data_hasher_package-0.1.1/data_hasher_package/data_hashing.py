import hashlib
import os
import re
import pandas as pd
from typing import Optional


class DataHasher:
    """
    A utility class for hashing data from files and verifying their integrity.

    Provides methods to create MD5 hashes for file contents and DataFrames,
    and to verify hashes embedded in filenames.
    """

    def __init__(self):
        pass

    @staticmethod
    def create_hash(file_path: str) -> str:
        """
        Generates an MD5 hash for the content of a given file.

        Args:
            file_path (str): Full path to the file.

        Returns:
            str: MD5 hash of the file's content.
        """
        hash_obj = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):  # Efficient chunk reading
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    @staticmethod
    def extract_hash_from_filename(filename: str) -> Optional[str]:
        """
        Extracts an MD5 hash embedded in the filename.

        Args:
            filename (str): Name of the file.

        Returns:
            Optional[str]: Extracted hash if found, otherwise None.
        """
        pattern = r"data_([a-fA-F0-9]{32})"
        match = re.search(pattern, filename)
        return match.group(1) if match else None

    @staticmethod
    def create_hash_from_dataframe(df: pd.DataFrame) -> str:
        """
        Generates an MD5 hash for the contents of a Pandas DataFrame.

        Args:
            df (pd.DataFrame): DataFrame to hash.

        Returns:
            str: MD5 hash of the DataFrame's content.
        """
        hash_obj = hashlib.md5()
        df_bytes = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
        hash_obj.update(df_bytes)
        return hash_obj.hexdigest()

    def verify_file_hash(self, file_path: str) -> bool:
        """
        Verifies if the hash extracted from the filename matches the file's content hash.

        Args:
            file_path (str): Full path to the file.

        Returns:
            bool: True if hashes match, otherwise False.
        """
        filename = os.path.basename(file_path)
        file_hash = self.create_hash(file_path)
        extracted_hash = self.extract_hash_from_filename(filename)
        return extracted_hash == file_hash
