# config_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import config
from logging_config import logger


class ConfigWindow(tk.Toplevel):
    def __init__(self, master: tk.Widget = None) -> None:
        super().__init__(master)
        self.title("Configuration")

        # StartGG Token row
        self.token_label = tk.Label(self, text="StartGG Token")
        self.token_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.token_entry = tk.Entry(self, width=32)
        self.token_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Load Config and Save Config buttons
        self.load_button = tk.Button(self, text="Load Config", command=self.load_config)
        self.load_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.save_button = tk.Button(self, text="Save Config", command=self.save_config)
        self.save_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Configure grid column weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load the current config into the UI
        self.load_config_into_ui()

    def load_config_into_ui(self) -> None:
        # Load the current config values into the UI fields
        self.token_entry.insert(0, config.current_config.get('startgg_token', ''))

    def load_config(self) -> None:
        # Open file dialog to select config file
        filename = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if filename:
            try:
                config.load_config_from_file(filename)
                self.load_config_into_ui()
                logger.info("Configuration loaded successfully.")
                messagebox.showinfo("Success", "Configuration loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                messagebox.showerror("Error", f"Failed to load config: {e}")

    def save_config(self) -> None:
        # Open file dialog to select where to save the config file
        filename = filedialog.asksaveasfilename(defaultextension=".yaml", filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if filename:
            try:
                # Update the current config with the values from the UI
                config.current_config['startgg_token'] = self.token_entry.get()
                config.save_config_to_file(filename)
                logger.info("Configuration saved successfully.")
                messagebox.showinfo("Success", "Configuration saved successfully.")
            except Exception as e:
                logger.error(f"Failed to save config: {e}")
                messagebox.showerror("Error", f"Failed to save config: {e}")
