import logging
import sys

VERBOSE = 3

LEVELS = {
    # 5: logging.DEBUG,
    # 4: logging.INFO,
    # 3: logging.WARNING,
    # 2: logging.ERROR,
    # 1: logging.CRITICAL
    3: logging.DEBUG,
    2: logging.INFO,
    1: logging.WARNING,
}


def __create_logger():
    # FIXME: correct log level
    # logLevel = LEVELS[VERBOSE]

    # # Formatter:
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # # FIXME: `allow file path parametrization`
    # # File handler:
    # fileHandler = logging.FileHandler("output.log")
    # fileHandler.setLevel(logLevel)
    # fileHandler.setFormatter(formatter)

    # # Stdout handler:
    # stdoutHandler = logging.StreamHandler(sys.stdout)
    # stdoutHandler.setLevel(logLevel)
    # stdoutHandler.setFormatter(formatter)

    # # Logger:
    # logger = logging.getLogger(__name__)
    # logger.addHandler(fileHandler)
    # logger.addHandler(stdoutHandler)
    # return logger
    logging.basicConfig(filename='output.log', level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")


LOGGER = __create_logger()


def log(msg, verbose=2, **kwargs):
    """
    Log message considering informed `verbose` parameter (min 1, max 3).
    """
    assert (verbose in LEVELS), "Invalid verbose option"
    # FIXME: consider `verbose` parameter
    # LOGGER.log(msg=msg, level=LEVELS[VERBOSE], **kwargs)
    # LOGGER.info(msg, **kwargs)
    logging.info(msg, **kwargs)


def log_err(msg=None, ex=None, **kwargs):
    assert (not msg is None) or (
        not ex is None), "Message or exception must be informed"
    if msg is None:
        msg = str(ex)
    # LOGGER.error(msg=msg, exc_info=True, stack_info=True, **kwargs)
    logging.error(msg=msg, exc_info=True, stack_info=True, **kwargs)


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


def auto_log_progress(iterable, total=None, message=None):
    from tqdm import tqdm
    return tqdm(iterable, total=total, desc=message)


def log_progress(current, total, message, **kwargs):
    log(f" [{current} / {total}] {message}",  **kwargs)
