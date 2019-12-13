def _logger(level):
    from logging import (
        DEBUG,
        INFO,
        CRITICAL,
        ERROR,
        getLogger,
        StreamHandler,
        Formatter,
        basicConfig,
        handlers,
    )

    # Set Log configurations
    basicConfig(
        format="%(asctime)s  ::  [%(levelname)s]  ::  %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        filename="rates.log",
        filemode="a",
        level=level.upper(),
    )

    logger = getLogger()
    handler = StreamHandler()
    logger.addHandler(handler)

    return logger
