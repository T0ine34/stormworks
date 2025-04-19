from .config import Config

CONFIG = Config("config.json")
_required = ["api", "api.port", "api.host", "app", "app.path", "resources"]
for r in _required:
    assert r in CONFIG, f"{r} key not found in config.json"