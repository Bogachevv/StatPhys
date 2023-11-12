import configloader
import py_singleton


@py_singleton.singleton
class ConfigLoader(object):
    def __init__(self):
        self._loader = configloader.ConfigLoader()
        self._path = "config.json"
        self.update()

    def update(self):
        with open(self._path, "r", encoding="utf-8") as f:
            self._loader.update_from_json_file(f)

    def __getitem__(self, item):
        return self._loader[item]
