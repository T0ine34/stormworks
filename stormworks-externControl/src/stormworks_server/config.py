import json5
from gamuLogger import Logger
import os

PATH = os.path.dirname(os.path.abspath(__file__))

class Config:
    def __init__(self, filepath : str|None = None):
        self.__filepath = filepath
        self.__config = {} # type: dict
        if filepath is not None:
            self.load()
        
    def load(self, path = None):
        if path is None:
            path = self.__filepath
        if path is None:
            raise ValueError("No file path provided")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r") as f:
            self.__config = json5.load(f)
        self.__filepath = path
    
    def save(self, path = None, pretty = False):
        if path is None:
            path = self.__filepath
        if path is None:
            raise ValueError("No file path provided")
        with open(path, "w") as f:
            json5.dump(self.__config, f, indent = 4 if pretty else None)
            
    def __getitem__(self, key):
        crt = self.__config
        for k in key.split("."):
            if isinstance(crt, dict):
                if k not in crt:
                    raise KeyError(f"Key not found: {key}")
                crt = crt[k]
            elif isinstance(crt, list):
                k = int(k)
                if k >= len(crt):
                    raise KeyError(f"Key not found: {key}")
                crt = crt[k]
            else:
                raise KeyError(f"Invalid key: {key}")
        return crt
    
    def __setitem__(self, key, value):
        crt = self.__config
        keys = key.split(".")
        for k in keys[:-1]:
            if isinstance(crt, dict):
                if k not in crt:
                    crt[k] = {}
                crt = crt[k]
            elif isinstance(crt, list):
                k = int(k)
                while len(crt) <= k:
                    crt.append({})
                crt = crt[k]
            else:
                raise ValueError(f"Invalid key: {key}")
        crt[keys[-1]] = value
        
    def __contains__(self, key):
        crt = self.__config
        for k in key.split("."):
            if isinstance(crt, dict):
                if k not in crt:
                    return False
                crt = crt[k]
            elif isinstance(crt, list):
                k = int(k)
                if k >= len(crt):
                    return False
                crt = crt[k]
            else:
                return False
        return True

    @property
    def filepath(self):
        return self.__filepath
    