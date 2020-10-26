from os import read
from os.path import normpath
from ..log import log

NEW_LINE = "\n"


def filter_files(dir, name="*", ext="*"):
    """Filter the files in the directory, based on the name and extension provided"""
    import glob
    assert (dir is not None), "`dir_path` is required"
    _ext = ext if ext.startswith(".") else f".{ext}"
    _path = normpath(f"{dir}/{name}{_ext}")
    return glob.glob(_path)


def create_if_missing(dir):
    """Create directory if it does not exist"""
    from pathlib import Path
    Path(dir).mkdir(parents=True, exist_ok=True)


def delete_dir(dir):
    """ Recursively remove a directory """
    from shutil import rmtree
    if exists(dir):
        rmtree(dir, ignore_errors=True)


def exists(path):
    from os.path import exists
    return exists(path)


def is_file(path):
    from os.path import isfile
    return exists(path) and isfile(path)


def is_dir(path):
    from os.path import isdir
    return exists(path) and isdir(path)


def read_json(path_or_dir, include_path=False):
    import json
    data = None

    def read_single(path, idx=0, total=1):
        """ Reads a single file """
        with open(path) as file:
            raw = json.load(file)
            return (raw, path) if include_path else raw

    def read_multiple(paths):
        """ Read multiple files from directory """
        total = len(paths)
        return [read_single(path, idx, total) for idx, path in enumerate(paths)]

    if is_file(path_or_dir):
        data = read_single(path_or_dir)
    elif is_dir(path_or_dir):
        paths = filter_files(path_or_dir, ext="json")
        data = read_multiple(paths)
    else:
        data = None
    return data


def read_items(path):
    """ Save the items into a file. """
    with open(path, "r", newline=NEW_LINE) as file:
        lines = file.readlines()
        return list(map(lambda x: x.replace(NEW_LINE, ""), lines))


def read_yaml(path):
    import yaml
    with open(path, 'r') as file:
        return yaml.full_load(file)


def save_json(data: dict, path: str):
    import json
    with open(path, 'w') as file:
        json.dump(data, file)


def save_yaml(data: dict, path: str):
    import yaml
    with open(path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, indent=4)


def save_items(items, path, append=False):
    """ Save the items into a file. """
    mode = "a" if append else "w"
    with open(path, mode, newline=NEW_LINE) as file:
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
    filename = basename(path)
    if not with_extension:
        filename = splitext(filename)[0]
    return filename

def normalize_path(path):
    from os.path import normpath
    return normpath(path)
