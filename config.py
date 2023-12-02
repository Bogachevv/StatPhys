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

    def set(self, key: str | tuple[str], value, check_key: bool = True):
        """
        Change record with key in config.
        It's not implemented by __setitem__ for config safety
        :param key: If key is str then changing cfg[key].
        If key is tuple (key_1, ..., key_n) then changing cfg[key_1][...][key_n]
        :param value: New value
        :param check_key: If true permit creating new elements
        """

        if check_key and not (key in self._loader):
            raise ValueError('check_key set to True, but key not in config keys')

        if isinstance(key, str):
            self._loader[key] = value
        else:
            to_update = self._loader
            for k in key[:-1]:
                to_update = to_update[k]
            to_update[key[-1]] = value
