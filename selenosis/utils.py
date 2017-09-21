def tag(*tags):
    """Decorator to add tags to a test class or method."""
    def decorator(obj):
        setattr(obj, 'tags', set(tags))
        return obj
    return decorator
