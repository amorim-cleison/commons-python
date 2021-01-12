import logging
import sys

VERBOSE = 1

LEVELS = {
    # 5: logging.DEBUG,
    # 4: logging.INFO,
    # 3: logging.WARNING,
    # 2: logging.ERROR,
    # 1: logging.CRITICAL
    3: logging.DEBUG,
    2: logging.INFO,
    1: logging.WARNING,
    # 2: logging.ERROR,
    # 1: logging.CRITICAL
}

def __create_logger():
    logLevel = LEVELS[VERBOSE]
    
    # Formatter:
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # File handler:
    fileHandler = logging.FileHandler("output.log")
    fileHandler.setLevel(logLevel)
    fileHandler.setFormatter(formatter)

    # Stdout handler:
    stdoutHandler = logging.StreamHandler(sys.stdout)
    fileHandler.setLevel(logLevel)
    fileHandler.setFormatter(formatter)

    # Logger:
    logger = logging.getLogger(__name__)
    logger.addHandler(fileHandler)
    logger.addHandler(stdoutHandler)
    return logger

LOGGER = __create_logger()


def log(msg, verbose=2, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 3).
    """
    assert (verbose in LEVELS), "Invalid verbose option"
    LOGGER.log(msg=msg, level=LEVELS[verbose], **kwargs)


def log_err(msg=None, ex=None, **kwargs):
    assert (not msg is None) or (
        not ex is None), "Message or exception must be informed"
    if msg is None:
        msg = str(ex)
    LOGGER.error(msg=msg, exc_info=True, stack_info=True, **kwargs)


def log_progress_bar(current, total, message=None, overwritable=False, **kwargs):
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
    log(text, end=end, **kwargs)


def log_progress(current, total, message, **kwargs):
    log(f" [{current} / {total}] {message}",  **kwargs)
