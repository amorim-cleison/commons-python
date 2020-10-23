VERBOSE = 3

def log(msg, verbose=1, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 3).
    """
    assert (0 < verbose <= 3), "Invalid verbose option"
    if verbose <= VERBOSE:
        print(msg, **kwargs)
