import json
import threading

from src.interfaces.repositories.session_interface import IDatabaseConnection

class DatabaseConnection(IDatabaseConnection):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, json_file_path):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, json_file_path):
        if getattr(self, "_initialized", False):
            return
        self.json_file_path = json_file_path
        self.data = None
        self._initialized = True

    def connect(self):
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = None
            print("Error: json file not found.")
