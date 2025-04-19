from stormworks_server.config import Config
import os
import pytest

class TestConfig:
    def test_load(self):
        config = Config()
        config.load("tests/server/test_config.json")
        assert config["test"] == "value"
        assert config["test2"] == 2
        assert config["test3"] == [1, 2, 3]
        assert config["test4"] == {"a": 1, "b": 2}
        
        
    def test_getitem_setitem(self):
        config = Config()
        config.load("tests/server/test_config.json")
        assert config["test"] == "value"
        assert config["test2"] == 2
        assert config["test3"] == [1, 2, 3]
        assert config["test4"] == {"a": 1, "b": 2}
        assert config["test3.1"] == 2
        
        with pytest.raises(KeyError):
            config["test5"]
        with pytest.raises(KeyError):
            config["test4.c"]
        with pytest.raises(KeyError):
            config["test4.a.b"]


    
    def test_save(self, tmp_path):
        config = Config()
        config["test"] = "value"
        config["test2"] = 2
        config["group.test1"] = 1
        config["group.test2"] = 2
        config["group.test3"] = 3
        config["group2.test1"] = 1
        config["group2.test2"] = 2
        config["group2.subgroup.test1"] = 1
        config["group2.subgroup.test2"] = 2
        
        config.save(tmp_path / "test_config.json")
        config2 = Config(tmp_path / "test_config.json")
        assert config2["test"] == "value"
        assert config2["test2"] == 2
        assert config2["group.test1"] == 1
        assert config2["group.test2"] == 2
        assert config2["group.test3"] == 3
        assert config2["group2.test1"] == 1
        assert config2["group2.test2"] == 2
        assert config2["group2.subgroup.test1"] == 1
        assert config2["group2.subgroup.test2"] == 2

    def test_contains(self):
        config = Config()
        config.load("tests/server/test_config.json")
        assert "test" in config
        assert "test2" in config
        assert "test5" not in config
        assert "test3.1" in config
        assert "test4.c" not in config
        assert "test4.a.b" not in config
        assert "group" in config
        assert "group.test1" in config
        assert "group.test3" in config
        assert "group2" in config
        assert "group2.test1" in config
        assert "group2.subgroup" in config
        assert "group2.subgroup.test1" in config

    def test_filepath(self):
        config = Config("tests/server/test_config.json")
        assert config.filepath == "tests/server/test_config.json"