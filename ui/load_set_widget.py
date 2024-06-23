import tkinter as tk
from tkinter import ttk
import threading
import queue
import api.startgg as startgg
from logging_config import logger

class LoadSetWidget(tk.Frame):
    def __init__(self, master: tk.Widget = None, main_window: 'MainWindow' = None) -> None:
        super().__init__(master)
        self.main_window = main_window  # Reference to MainWindow instance

        self.label = tk.Label(self, text="Set ID")
        self.label.pack(side="left", padx=5)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var, validate="key", validatecommand=(self.register(self.validate_number), '%P'))
        self.entry.pack(side="left", padx=5)

        self.button = tk.Button(self, text="Load Set", command=self.load_set)
        self.button.pack(side="left", padx=5)

        self.result_queue = queue.Queue()  # Create a queue for thread results

    def validate_number(self, value_if_allowed: str) -> bool:
        # Allow empty string or numbers only
        if value_if_allowed == "" or value_if_allowed.isdigit():
            return True
        else:
            return False

    def load_set(self) -> None:
        set_id = self.entry_var.get()
        if set_id.isdigit():
            logger.info(f"Loading set with ID: {set_id}")
            self.main_window.update_status("Querying StartGG for set details...", "info")
            threading.Thread(target=self.perform_query, args=(int(set_id),)).start()
            self.after(100, self.check_thread_result)  # Check the queue periodically
        else:
            self.main_window.update_status("Invalid Input: Please enter a valid Set ID", "error")

    def perform_query(self, set_id: int) -> None:
        try:
            result = startgg.get_set(set_id)
            self.result_queue.put(result)  # Put the result into the queue
        except startgg.NoApiKey as e:
            self.result_queue.put(e)
        except Exception as e:
            self.result_queue.put(e)

    def check_thread_result(self):
        try:
            result = self.result_queue.get_nowait()  # Retrieve result from the queue
            if isinstance(result, Exception):
                if isinstance(result, startgg.NoApiKey):
                    logger.error(f"No StartGG API key error: {result}")
                    self.main_window.update_status("No StartGG API key error: Please configure your StartGG API key", "error")
                else:
                    logger.error(f"An error occurred while retrieving set details: {result}")
                    self.main_window.update_status(f"An error occurred: {result}", "error")
            else:
                if result and result.get('set'):
                    logger.info(f"Set details retrieved successfully: {result}")
                    self.main_window.startgg_set = result  # Assign the result to startgg_set
                    self.main_window.update_status("Set details retrieved successfully", "success")
                    self.main_window.update_set_frame()  # Update the SetFrame
                else:
                    logger.error("No set found with that ID")
                    self.main_window.update_status("No set found with that ID. Please check the Set ID and try again.", "error")
        except queue.Empty:
            self.after(100, self.check_thread_result)  # Continue checking the queue
