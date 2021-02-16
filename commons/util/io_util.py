NEW_LINE = "\n"


def filter_files(dir, name="*", ext="*", recursive=False, path_as_str=True):
    """Filter the files in the directory, based on the name and extension provided"""
    assert (dir is not None), "`dir_path` is required"
    _ext = ext if ext.startswith(".") else f".{ext}"

    if recursive:
        fn = __get_path(dir).rglob
    else:
        fn = __get_path(dir).glob
    result = list(fn(f"{name}{_ext}"))
    return __parse_result(result, path_as_str)


def create_if_missing(dir):
    """Create directory if it does not exist"""
    __get_path(dir).mkdir(parents=True, exist_ok=True)


def delete_file(path):
    if exists(path):
        assert is_file(path), "Path must be a file"
        __get_path(path).unlink()


def delete_dir(dir):
    """ Recursively remove a directory """
    from shutil import rmtree
    _dir = normpath(dir)
    if exists(_dir):
        assert is_dir(dir), "Path must be a directory"
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
        paths = filter_files(_path, ext="json", path_as_str=False)
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
        content = NEW_LINE.join(items + [""])
        file.write(content)


def is_downloadable(url):
    from requests import get
    return get(url, stream=True).ok


def download_file(url, target_file, progress_bar=False):
    from requests import get
    from commons.log import auto_log_progress

    try:
        response = get(url, stream=True)
        response.raise_for_status()

        with open(target_file, 'wb') as f:
            chunk_size = 1024
            iterable = response.iter_content(chunk_size=chunk_size)

            if progress_bar:
                file_length = int(response.headers.get('content-length', 0))
                total = int(file_length/chunk_size)
                iterable = auto_log_progress(iterable, total=total)

            for chunk in iterable: 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return response.ok, None
    except Exception as e:
        return False, e


def filename(path, with_extension=True):
    from os.path import splitext, basename
    filename = basename(normpath(path))
    if not with_extension:
        filename = splitext(filename)[0]
    return filename


def extension(path):
    return "".join(normpath(path, False).suffixes)


def directory(path, path_as_str=True):
    return __parse_result(__get_path(path).parent, path_as_str)


def normpath(path, path_as_str=True):
    return __parse_result(__get_path(path), path_as_str)


def __get_path(path):
    from pathlib import Path
    return Path(path).expanduser().resolve()


def __parse_result(path, path_as_str=True):
    if path_as_str:
        if isinstance(path, list):
            return [str(x) for x in path]
        if isinstance(path, set):
            return {str(x) for x in path}
        else:
            return str(path)
    else:
        return path
