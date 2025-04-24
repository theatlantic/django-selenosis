def tag(*tags):
    """Decorator to add tags to a test class or method."""

    def decorator(obj):
        setattr(obj, "tags", set(tags))
        return obj

    return decorator


class class_property:
    "Like the property builtin, but as a classmethod"

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None and objtype is None:
            return self
        objtype = objtype or type(obj)
        if self.fget is None:
            raise AttributeError
        return self.fget(objtype)
