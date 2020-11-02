NEW_LINE = "\n"


def filter_files(dir, name="*", ext="*", recursive=False, as_str=True):
    """Filter the files in the directory, based on the name and extension provided"""
    assert (dir is not None), "`dir_path` is required"
    _ext = ext if ext.startswith(".") else f".{ext}"

    if recursive:
        fn = __get_path(dir).rglob
    else:
        fn = __get_path(dir).glob
    result = list(fn(f"{name}{_ext}"))
    return __parse_result(result, as_str)


def create_if_missing(dir):
    """Create directory if it does not exist"""
    __get_path(dir).mkdir(parents=True, exist_ok=True)


def delete_dir(dir):
    """ Recursively remove a directory """
    from shutil import rmtree
    _dir = normpath(dir)
    if exists(_dir):
        rmtree(_dir, ignore_errors=True)


def exists(path):
    return __get_path(path).exists()


def is_file(path):
    return exists(path) and __get_path(path).is_file()


def is_dir(path):
    return exists(path) and __get_path(path).is_dir()


def read_json(path_or_dir, include_path=False):
    import json
    data = None
    _path = __get_path(path_or_dir)

    def read_single(path):
        """ Reads a single file """
        with path.open() as file:
            raw = json.load(file)
            return (raw, path) if include_path else raw

    def read_multiple(paths):
        """ Read multiple files from directory """
        return [read_single(path) for path in paths]

    if _path.is_file():
        data = read_single(_path)
    elif _path.is_dir():
        paths = filter_files(_path, ext="json", as_str=False)
        data = read_multiple(paths)
    else:
        data = None
    return data


def read_items(path):
    """ Save the items into a file. """
    with __get_path(path).open("r", newline=NEW_LINE) as file:
        lines = file.readlines()
        return list(map(lambda x: x.replace(NEW_LINE, ""), lines))


def read_yaml(path):
    import yaml
    with __get_path(path).open('r') as file:
        return yaml.full_load(file)


def save_json(data: dict, path: str):
    import json
    with __get_path(path).open('w') as file:
        json.dump(data, file)


def save_yaml(data: dict, path: str):
    import yaml
    with __get_path(path).open('w') as file:
        yaml.dump(data, file, default_flow_style=False, indent=4)


def save_items(items, path, append=False):
    """ Save the items into a file. """
    mode = "a" if append else "w"
    with __get_path(path).open(mode, newline=NEW_LINE) as file:
        file.write(NEW_LINE.join(items))


def download_file(url, target_file):
    from urllib.request import urlretrieve
    try:
        urlretrieve(url, target_file)
        return is_file(target_file), None
    except Exception as e:
        return False, str(e)


def filename(path, with_extension=True):
    from os.path import splitext, basename
    filename = basename(normpath(path))
    if not with_extension:
        filename = splitext(filename)[0]
    return filename


def normpath(path, as_str=True):
    return __parse_result(__get_path(path), as_str)


def __get_path(path):
    from pathlib import Path
    return Path(path).expanduser().absolute()

def __parse_result(path, as_str=True):
    from pathlib import Path
    if as_str:
        if isinstance(path, list):
            return [str(x) for x in path]
        else:
            return str(path)
    else:
        return path
