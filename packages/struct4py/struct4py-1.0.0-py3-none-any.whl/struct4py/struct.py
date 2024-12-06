class Struct:
    def __init__(self):
        self.__dict__["_storage"] = {}

    def __getattr__(self, name):
        if name not in self._storage:
            # Create a new Struct instance if the attribute doesn't exist
            self._storage[name] = Struct()
        elif not isinstance(self._storage[name], Struct):
            # Return the real value if it's not a Struct (no more subnodes)
            return self._storage[name]
        return self._storage[name]

    def __setattr__(self, name, value):
        self._storage[name] = value

    def __repr__(self):
        return "Struct(" + repr(self._storage) + ")"

    def to_dict(self):
        def convert(obj):
            if isinstance(obj, Struct):
                return {key: convert(value) for key, value in obj._storage.items()}
            return obj

        return convert(self)
