# logging_config.py
import logging

# Create a file handler with utf-8 encoding
file_handler = logging.FileHandler("app.log", encoding='utf-8')

# Create a stream handler for console output
stream_handler = logging.StreamHandler()

# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)

# Get the logger for your module
logger = logging.getLogger(__name__)
