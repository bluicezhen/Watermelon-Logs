import logging


def get_logger(level: int = logging.DEBUG, stream_out: bool = True, file_path: str = None) -> logging.Logger:
    """ Get My Logger Function
    https://gist.github.com/bluicezhen/2e43035a52fd1be77669ed27a38d4b32

    :param level:       Log level.
    :param stream_out:  Whether write log to stream.
    :param file_path:   File path to  write log to. If none, no log file
    :return: Logger object
    """
    logger = logging.Logger(__name__)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)7s: %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    if stream_out:
        sh = logging.StreamHandler(stream=None)
        sh.setLevel(level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    if file_path:
        fh = logging.FileHandler(file_path, mode='a', encoding="utf-8", delay=False)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


if __name__ == "__main__":
    my_logger = get_logger(file_path="t.log")
    my_logger.debug("hello world")
    my_logger.info("hello world")
    my_logger.warning("hello world")
    my_logger.error("hello world")
