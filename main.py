import logging
from ui.main_window import MainWindow
from logging_config import logger

if __name__ == "__main__":
    logger.info("Starting the application")
    app = MainWindow()
    app.run()
    logger.info("Application has stopped")
