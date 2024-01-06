def singleton(cls):
    _instances = {}

    def instance(*args, **kwargs) -> cls:
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    
    return instance