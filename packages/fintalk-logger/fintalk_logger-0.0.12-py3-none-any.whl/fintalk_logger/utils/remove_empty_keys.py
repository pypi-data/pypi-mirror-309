def remove_empty_keys(data):
    obj = data
    if not isinstance(data, dict) or not data:
        return data
    for key in obj.keys():
        if obj[key] and isinstance(obj[key], dict):
            remove_empty_keys(obj[key])
        elif obj[key] is None:
            del obj[key]
    return obj