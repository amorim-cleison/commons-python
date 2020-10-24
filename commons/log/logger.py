VERBOSE = 3

def log(msg, verbose=1, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 3).
    """
    assert (0 < verbose <= 3), "Invalid verbose option"
    if verbose <= VERBOSE:
        print(msg, **kwargs)


def log_progress(current, total, message=None, overwritable=False):
    increments = 50
    percentual = ((current / total) * 100)
    i = int(percentual // (100 / increments))
    prefix = f"{message} " if message else ""
    text = "\r{}|{: <{}}| {:.0f}%".format(prefix, '█' * i, increments,
                                          percentual)

    if overwritable:
        end = "\r"
    elif percentual >= 100:
        end = "\n"
    else:
        end = ""
    log(text, 1, end=end)
