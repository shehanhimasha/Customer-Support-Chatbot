import json
from pathlib import Path

class DataLoader:
    """
    Loading JSON data from the /data folder.
   
    """

    def __init__(self, data_path="data"):
        # Convert folder path to a Path object for easier operations
        self.data_path = Path(data_path)

    def load_json(self, file_name):
        """
        Loads any JSON file in the /data directory.
        
        Parameters:
            file_name (str): Name of the JSON file (e.g., 'orders.json')

        Returns:
            list/dict: Parsed JSON content
        """
        file_path = self.data_path / file_name
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_name}")
            return []
        except json.JSONDecodeError:
            print(f"[ERROR] JSON format issue in {file_name}")
            return []
