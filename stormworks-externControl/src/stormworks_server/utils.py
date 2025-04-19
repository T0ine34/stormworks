import os
from gamuLogger import Logger
import datetime as dt

def getMIMEType(path):
    if path.endswith(".html"):
        return "text/html"
    elif path.endswith(".css"):
        return "text/css"
    elif path.endswith(".js"):
        return "application/javascript"
    elif path.endswith(".json"):
        return "application/json"
    elif path.endswith(".png"):
        return "image/png"
    elif path.endswith(".jpg"):
        return "image/jpg"
    elif path.endswith(".jpeg"):
        return "image/jpeg"
    elif path.endswith(".gif"):
        return "image/gif"
    elif path.endswith(".svg"):
        return "image/svg+xml"
    elif path.endswith(".ico"):
        return "image/x-icon"
    elif path.endswith(".map"):
        return "application/json"
    elif path.endswith(".ttf"):
        return "font/ttf"
    else:
        Logger.warning(f"Unknown MIME type for {path}")
        return "application/octet-stream"
    

def getFileName(path):
    if os.path.exists(path):
        return path
    for ext in ["", ".html", ".js", ".css"]:
        if os.path.exists(f"{path}{ext}"):
            return f"{path}{ext}"
    raise FileNotFoundError(f"File not found: {path}")

def splitchars(string : str, sep : str) -> str:
    return sep.join(string)