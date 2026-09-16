class KVSTORE:
    def __init__(self):
        self._map = dict()

    def get(self, key: bytes):
        return self._map.get(key)

    def set(self, key: bytes, value: bytes):
        self._map[key] = value
