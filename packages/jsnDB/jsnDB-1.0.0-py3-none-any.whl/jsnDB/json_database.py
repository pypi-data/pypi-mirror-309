import logging
import json
from pathlib import Path



class JsonDB:
    """A lightweight JSON-based database."""

    def __init__(self, filename: str = "db.json", enable_logging: bool = True):
        """
        Initialize the database.

        :param filename: Name of the JSON database file.
        :param enable_logging: Enable or disable logging.
        """
        self.file = Path(filename)
        self.db = self._initialize_file()
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.DEBUG if enable_logging else logging.WARNING,
        )
        logging.info("Database initialized.")

    def _initialize_file(self) -> dict:
        """Ensure the database file exists and is valid JSON."""
        if not self.file.exists():
            self.file.write_text("{}") 
        try:
            return json.loads(self.file.read_text())
        except json.JSONDecodeError:
            logging.error("Database file contains invalid JSON.")

    def _write_to_file(self):
        """Write the current database state to the file."""
        try:
            self.file.write_text(json.dumps(self.db, indent=4))
            logging.info("Database committed to file.")
        except Exception as e:
            logging.error(f"Failed to write to file: {e}")

    def add(self, key: str, value: any):
        """
        Add or update a key-value pair in the database.

        :param key: The key to add or update.
        :param value: The value to associate with the key.
        """
        self.db[key] = value
        logging.info(f"Added/Updated key: {key}, Value: {value}")
    def addMany(self, data : dict):
        """Add or update multiple entries in the database
        :param data: The dict to add or update
        """
        self.db.update(data)
        logging.info(f"Added/Updated {data} in the database")

    def pop(self, key: str):
        """
        Remove a key-value pair from the database.

        :param key: The key to remove.
        :raises KeyError: If the key does not exist in the database.
        """
        if key in self.db:
            self.db.pop(key)
            logging.info(f"Popped key: {key}")
        else:
            logging.error(f"Key '{key}' not found in database.")
            raise KeyError(f"Key '{key}' not found.")

    def get(self, key: str) -> any:
        """
        Retrieve a value from the database by key.

        :param key: The key to retrieve.
        :return: The value associated with the key.
        :raises KeyError: If the key does not exist in the database.
        """
        if key in self.db:
            return self.db[key]
        else:
            logging.error(f"Key '{key}' not found in database.")
            raise KeyError(f"Key '{key}' not found.")

    def get_all(self) -> dict:
        """
        Get the entire database.

        :return: A dictionary representing the database.
        """
        logging.info("Fetched the entire database.")
        return self.db

    def commit(self):
        """Commit the current state of the database to the file."""
        self._write_to_file()

    def close(self):
        """Close database by clearing all entries"""
        self.db.clear()
        logging.info("Closed the database.")

    def set_logging(self, enable: bool):
        """
        Enable or disable logging.

        :param enable: True to enable debug-level logging, False for warnings only.
        """
        logging.getLogger().setLevel(logging.DEBUG if enable else logging.WARNING)
        