VERBOSE = 3


def log(msg, verbose=1, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 3).
    """
    assert (0 < verbose <= 3), "Invalid verbose option"
    if verbose <= VERBOSE:
        print(msg, **kwargs)


def log_err(msg=None, ex=None, **kwargs):
    import traceback
    assert (not msg is None) or (
        not ex is None), "Message or exception must be informed"
    if msg is None:
        msg = str(ex)
    log(msg, verbose=1, **kwargs)
    traceback.print_exc()


def log_progress_bar(current, total, message=None, overwritable=False, **kwargs):
    increments = 50
    percentual = ((current / total) * 100)
    i = int(percentual // (100 / increments))
    prefix = f"{message[:30]} " if message else ""
    text = "\r{}|{: <{}}| {:.0f}%".format(prefix, '█' * i, increments,
                                          percentual)

    if overwritable:
        end = "\r"
    elif percentual >= 100:
        end = "\n"
    else:
        end = ""
    log(text, end=end, **kwargs)


def log_progress(current, total, message, **kwargs):
    log(f" [{current} / {total}] {message}",  **kwargs)
