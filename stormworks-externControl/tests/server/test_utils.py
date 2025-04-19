import pytest
from stormworks_server.utils import getMIMEType, getFileName
from time import sleep
    
class TestgetMIMEType:
    @pytest.mark.parametrize("path, expected", [
        ("index.html", "text/html"),
        ("styles.css", "text/css"),
        ("app.js", "application/javascript"),
        ("data.json", "application/json"),
        ("image.png", "image/png"),
        ("photo.jpg", "image/jpg"),
        ("photo.jpeg", "image/jpeg"),
        ("animation.gif", "image/gif"),
        ("vector.svg", "image/svg+xml"),
        ("favicon.ico", "image/x-icon"),
        ("source.map", "application/json"),
        ("font.ttf", "font/ttf"),
        ("unknownfile.xyz", "application/octet-stream")
    ])
    def test_getMIMEType(self, path, expected):
        assert getMIMEType(path) == expected
        
    
class TestgetFileName:
    def test_getFileName(self):
        with pytest.raises(FileNotFoundError):
            getFileName("nonexistentfile")
        assert getFileName("tests/server/test_config.json") == "tests/server/test_config.json"

