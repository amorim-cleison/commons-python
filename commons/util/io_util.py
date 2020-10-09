from os.path import normpath
from ..log import log


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


def exists(path):
    from os.path import isfile
    return isfile(path)


def is_file(path):
    from os.path import isdir
    return exists(path) and not isdir(path)


def is_dir(path):
    from os.path import isdir
    return exists(path) and isdir(path)


def read_json(path_or_dir, include_path=False):
    import json
    all_content = list()
    files = list()

    if is_file(path_or_dir):
        files = path_or_dir
    elif is_dir(path_or_dir):
        files = filter_files(dir, ext="json")

    total = len(files)

    for idx, path in enumerate(files):
        log(f" [{idx + 1} / {total}] Reading '{path}'...", 2)

        with open(path) as file:
            raw = json.load(file)
            content = (raw, path) if include_path else raw
            all_content.append(content)
    return all_content
