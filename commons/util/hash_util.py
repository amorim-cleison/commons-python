def get_hash(o):
    from json import dumps
    from hashlib import md5
    data = dumps(o, sort_keys=True, ensure_ascii=False,
                 indent=None).encode('utf-8')
    return md5(data).digest().hex()
