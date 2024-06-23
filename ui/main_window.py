# main_window.py
import logging
import tkinter as tk
from ui.load_set_widget import LoadSetWidget
from ui.set_frame import SetFrame
from ui.config_window import ConfigWindow
from logging_config import logger
from ui.tweet_set_window import TweetSetWindow

class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PFGG Tournament Social")

        self.startgg_set = None  # Initialize startgg_set in MainWindow

        # LoadSetWidget
        self.load_set_widget = LoadSetWidget(self.root, main_window=self)
        self.load_set_widget.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # Tweet Set button
        self.tweet_set_button = tk.Button(self.root, text="Tweet Set", command=self.open_tweet_set_window)
        self.tweet_set_button.grid(row=0, column=1, pady=20, padx=20, sticky="w")

        # SetFrame placeholder
        self.set_frame = SetFrame(self.root)
        self.set_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        # Status label
        self.status_label = tk.Label(self.root, text="", anchor="w", width=50)
        self.status_label.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        # Button to open config window
        self.config_button = tk.Button(self.root, text="Config", command=self.open_config_window)
        self.config_button.grid(row=2, column=1, pady=20, padx=20, sticky="e")

        # Configure grid column weights for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        self.config_window = None
        self.tweet_set_window = None

    def open_tweet_set_window(self) -> None:
        if self.tweet_set_window is None or not self.tweet_set_window.winfo_exists():
            self.tweet_set_window = TweetSetWindow(self.root, self)
        else:
            self.tweet_set_window.lift()
            logger.info("Tweet Set window is already open and brought to front")

    def tweet_set(self) -> None:
        self.open_tweet_set_window()

    def open_config_window(self) -> None:
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = ConfigWindow(self.root)
        else:
            self.config_window.lift()
            logger.info("Config window is already open and brought to front")

    def update_status(self, message: str, level: str) -> None:
        colors = {
            "info": "black",
            "warning": "orange",
            "error": "red",
            "success": "green"
        }
        color = colors.get(level, "black")
        self.status_label.config(text=message, fg=color)
        logger.log({"info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO), message)

    def update_set_frame(self) -> None:
        # Update the SetFrame with the new set data
        if self.startgg_set:
            self.set_frame.update_set_data(self.startgg_set)
            if self.tweet_set_window is not None and self.tweet_set_window.winfo_exists():
                logger.info("Tweet Set window is already open, no need to update")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.run()
