import logging
import logging.config

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a handler that will save logs to a file
logger_handler = logging.FileHandler(filename="core.log", mode="w", encoding="utf-8")
logger_handler.setLevel(logging.DEBUG)

# Create a formatter for saved logs and add it to the handler
logging_formatter = logging.Formatter("%(asctime)s %(name)s-%(levelname)s:%(message)s")
logger_handler.setFormatter(logging_formatter)

# Now add the handler to the original logger
logger.addHandler(logger_handler)
logging.info("Logger configured successfully!")