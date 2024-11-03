import logging

def setup_logger(name=__name__, log_file='/Users/usarneme/Library/Logs/hackernews_scraper.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if logger already has handlers (to avoid duplication)
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter and set it for both handlers
        formatter = logging.Formatter(f'%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger