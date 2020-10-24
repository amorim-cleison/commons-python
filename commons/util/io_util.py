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
    all_content = list()

    if is_file(path_or_dir):
        files = [path_or_dir]
    elif is_dir(path_or_dir):
        files = filter_files(path_or_dir, ext="json")
    else:
        files = []

    total = len(files)

    for idx, path in enumerate(files):
        log(f" [{idx + 1} / {total}] Reading '{path}'...", 3)

        with open(path) as file:
            raw = json.load(file)
            content = (raw, path) if include_path else raw
            all_content.append(content)
    return all_content


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


def save_items(items, path):
    """ Save the items into a file. """
    import os
    with open(path, 'w') as file:
        # Write dict:
        if isinstance(items, list):
            for key, val in items.items():
                file.write(f"{key}:{val}{os.linesep}")

        # Write other iterables:
        else:
            for item in items:
                file.write(f"{item}{os.linesep}")


def download_file(url, target_file):
    from urllib.request import urlretrieve
    log(f"Downloading '{url}' to '{target_file}'...", 2)
    urlretrieve(url, target_file)
    return is_file(target_file)
