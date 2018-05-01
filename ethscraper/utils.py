def hex_to_dec(str):
    if str is None:
        return None
    try:
        return int(str, 16)
    except ValueError:
        print ("Not a hex string %s" % str)
        return str


def without_key(dictionary, key):
    return {k: dictionary[k] for k in dictionary if k != key}


def chunk_string(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def str2bool(obj):
    if isinstance(obj, basestring):
        return obj.lower() in ("yes", "true", "t", "1")
    else:
        return obj
