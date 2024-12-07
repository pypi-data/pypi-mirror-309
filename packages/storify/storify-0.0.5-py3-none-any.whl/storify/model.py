class Model:
    @property
    def _key(self):
        return f"__{self.__class__.__name__}__"

    @classmethod
    def _keyname(cls):
        return f"__{cls.__name__}__"
    
    def _to_dict(self):
        filtered_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return {
            self._key: filtered_dict
        }

    def _from_dict(self, data):
        if self._key in data:
            self.__dict__.update(data[self._key])

        return self

    @classmethod
    def _deserialize(cls, data):
        return cls._from_dict(data)