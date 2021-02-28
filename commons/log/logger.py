import logging

LEVELS = {
    5: logging.DEBUG,
    4: logging.INFO,
    3: logging.WARNING,
    2: logging.ERROR,
    1: logging.CRITICAL,
    0: logging.NOTSET
}

LOG_INITIALIZED = False


def init_logger(args):
    def setup_log(log, verbosity, **kwargs):
        if log is not None:
            assert (verbosity in LEVELS), "Invalid verbosity option"
            logging.basicConfig(
                filename=log,
                level=LEVELS[verbosity],
                format="%(asctime)s - %(levelname)s - %(message)s")

    args = args if isinstance(args, dict) else vars(args)
    setup_log(**args)
    global LOG_INITIALIZED
    LOG_INITIALIZED = True


def __verify_logger():
    assert LOG_INITIALIZED, "Logger was not initialized. Please, make\
        sure to initialize it calling `logger.init` method."


def log(msg, verbose=4, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 5).
    """
    __verify_logger()
    # logging.log(msg=msg, level=LEVELS[verbose], **kwargs)
    logging.info(msg=msg, **kwargs)
    print(msg, **kwargs)


def log_err(msg=None, ex=None, **kwargs):
    assert (msg is not None) or (
        ex is not None), "Message or exception must be informed"
    if msg is None:
        msg = str(ex)
    __verify_logger()
    logging.error(msg=msg, exc_info=True, stack_info=True, **kwargs)
    print(msg, **kwargs)


def log_progress_bar(current,
                     total,
                     message=None,
                     overwritable=False,
                     **kwargs):
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


def auto_log_progress(iterable, total=None, message=None):
    from tqdm import tqdm
    return tqdm(iterable, total=total, desc=message)


def log_progress(current, total, message, **kwargs):
    log(f" [{current} / {total}] {message}", **kwargs)
