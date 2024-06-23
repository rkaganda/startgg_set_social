# tweet_set_window.py
import yaml
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
from logging_config import logger

class TweetSetWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, main_window: 'MainWindow'):
        super().__init__(master)
        self.main_window = main_window  # Store reference to MainWindow
        self.title("Tweet Set")

        try:
            # Load tweet templates from YAML file with UTF-8 encoding
            with open('templates/tweets.yaml', 'r', encoding='utf-8') as file:
                self.tweet_templates = yaml.safe_load(file)
            logger.info("Tweet templates loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load tweet templates: {e}")
            self.main_window.update_status(f"Error loading tweet templates: {e}", "error")
            return

        # Dropdown for tweet templates
        self.selected_template = tk.StringVar(self)
        self.template_dropdown = ttk.Combobox(self, textvariable=self.selected_template)
        self.template_dropdown['values'] = list(self.tweet_templates.keys())
        if self.template_dropdown['values']:
            self.template_dropdown.current(0)  # Set default value to the first template
        self.template_dropdown.grid(row=0, column=1, pady=10, padx=10)

        # Label for template selection
        self.template_label = tk.Label(self, text="Select tweet template:")
        self.template_label.grid(row=0, column=0, pady=10, padx=10)

        # Preview Tweet button
        self.preview_button = tk.Button(self, text="Preview Tweet", command=self.preview_tweet)
        self.preview_button.grid(row=1, column=0, pady=10, padx=10)

        # Copy Tweet button
        self.copy_button = tk.Button(self, text="Copy Tweet", command=self.copy_tweet)
        self.copy_button.grid(row=1, column=1, pady=10, padx=10)

    def preview_tweet(self) -> None:
        try:
            selected_template = self.selected_template.get()
            tweet_mappings = self.map_tweet_template(self.main_window.startgg_set)
            tweet_text = self.tweet_templates[selected_template].format(**tweet_mappings)
            messagebox.showinfo("Tweet Preview", tweet_text)  # Show tweet text in a dialog
            logger.info(f"Tweet preview: {tweet_text}")
        except Exception as e:
            logger.error(f"Failed to preview tweet: {e}")
            self.main_window.update_status(f"Error previewing tweet: {e}", "error")

    def copy_tweet(self) -> None:
        try:
            selected_template = self.selected_template.get()
            tweet_mappings = self.map_tweet_template(self.main_window.startgg_set)
            tweet_text = self.tweet_templates[selected_template].format(**tweet_mappings)
            self.clipboard_clear()
            self.clipboard_append(tweet_text)
            self.update()  # Keep the clipboard contents after the window is closed
            logger.info("Tweet copied to clipboard")
            self.main_window.update_status("Tweet copied to clipboard", "success")
        except Exception as e:
            logger.error(f"Failed to copy tweet: {e}")
            self.main_window.update_status(f"Error copying tweet: {e}", "error")

    @staticmethod
    def create_entrants_string(startgg_set: Dict) -> str:
        try:
            def get_participant_string(participant: Dict) -> str:
                authorizations = participant['user'].get('authorizations', [])
                twitter_auth = next((auth for auth in authorizations if auth['type'] == 'TWITTER'), None)
                if twitter_auth:
                    return f"@{twitter_auth['externalUsername']}"
                else:
                    return participant['gamerTag']

            slots = startgg_set['set']['slots']
            participants_strings = [get_participant_string(slot['entrant']['participants'][0]) for slot in slots]
            entrants_string = " vs ".join(participants_strings)
            return entrants_string
        except Exception as e:
            logger.error(f"Failed to create entrants string: {e}")
            raise

    @staticmethod
    def map_tweet_template(startgg_set: Dict) -> Dict:
        try:
            # Create the tweet_mappings dictionary and
            # Assign the 'entrants' key the return value of create_entrants_string
            tweet_mappings = {'entrants': TweetSetWindow.create_entrants_string(startgg_set)}

            # Assign the 'event_url' key
            event_slug = startgg_set['set']['event'].get('slug', "")
            tweet_mappings['event_url'] = f"https://www.start.gg/{event_slug}" if event_slug else ""

            # Assign the 'event_name' key
            tweet_mappings['event_name'] = startgg_set['set']['event']['tournament'].get('name', "")

            # Assign the 'stream_urls' key
            stream = startgg_set['set'].get('stream', {})
            stream_urls = []
            if stream.get('streamSource') == 'TWITCH':
                stream_urls.append(f"https://www.twitch.tv/{stream['streamName']}")
            tweet_mappings['stream_urls'] = ', '.join(stream_urls)

            # Load the game hashtags from a YAML file
            with open('templates/game_hashtags.yaml', 'r') as file:
                game_hashtags = yaml.safe_load(file)

            # Assign the 'game' key
            videogame_name = startgg_set['set']['event']['videogame']['name']
            tweet_mappings['game'] = game_hashtags.get(videogame_name, "")

            logger.info("Tweet mappings created successfully")
            print(tweet_mappings)
            return tweet_mappings
        except Exception as e:
            logger.error(f"Failed to map tweet template: {e}")
            raise
