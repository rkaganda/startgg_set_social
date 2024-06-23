import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional

class SlotFrame(tk.Frame):
    def __init__(self, master: tk.Widget = None, slot: Dict = None) -> None:
        super().__init__(master)
        self.slot = slot

        # Display the standing score
        score_value = self.slot['standing']['stats']['score']['value']
        self.score_label = tk.Label(self, text=f"Score: {score_value}")
        self.score_label.pack(anchor="w")

        # Process each entrant in the slot
        self.create_entrant_widgets(self.slot['entrant'])

    def create_entrant_widgets(self, entrant: Dict) -> None:
        # Display the entrant name
        entrant_name = entrant['name']
        self.name_label = tk.Label(self, text=f"Entrant: {entrant_name}")
        self.name_label.pack(anchor="w")

        # Create the table for authorizations
        self.table = ttk.Treeview(self, columns=("Type", "Username"), show="headings")
        self.table.heading("Type", text="Type")
        self.table.heading("Username", text="Username")
        self.table.pack(fill="x", expand=True)

        # Insert authorizations into the table
        authorizations = entrant['participants'][0]['user']['authorizations']
        if authorizations:
            for auth in authorizations:
                self.table.insert("", "end", values=(auth['type'], auth['externalUsername']))

class SetFrame(tk.Frame):
    def __init__(self, master: tk.Widget = None, set_data: Optional[Dict] = None) -> None:
        super().__init__(master)
        self.set_data = set_data
        self.create_widgets()

    def create_widgets(self) -> None:
        if self.set_data:
            slots = self.set_data['set']['slots']
            for slot in slots:
                slot_frame = SlotFrame(self, slot=slot)
                slot_frame.pack(side="left", padx=10, pady=10, fill="y")
        else:
            self.no_data_label = tk.Label(self, text="No set data available")
            self.no_data_label.pack()

    def update_set_data(self, set_data: Dict) -> None:
        self.set_data = set_data
        self.clear_widgets()
        self.create_widgets()

    def clear_widgets(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Set Details")

    # Example set data
    set_data = {
        'set': {
            'id': 76008467,
            'slots': [
                {
                    'entrant': {
                        'id': 16922875,
                        'name': 'knotts',
                        'participants': [{
                            'id': 15722048,
                            'gamerTag': 'knotts',
                            'user': {
                                'authorizations': [
                                    {'type': 'TWITTER', 'externalUsername': 'Knottts'},
                                    {'type': 'DISCORD', 'externalUsername': 'Knotts#0002'},
                                    {'type': 'TWITCH', 'externalUsername': 'Knottss'}
                                ]
                            }
                        }]
                    },
                    'standing': {'stats': {'score': {'value': 2}}}
                },
                {
                    'entrant': {
                        'id': 16923086,
                        'name': 'Luusei',
                        'participants': [{
                            'id': 15722224,
                            'gamerTag': 'Luusei',
                            'user': {
                                'authorizations': [
                                    {'type': 'TWITTER', 'externalUsername': 'Luusei_'}
                                ]
                            }
                        }]
                    },
                    'standing': {'stats': {'score': {'value': 0}}}
                }
            ]
        }
    }

    set_frame = SetFrame(root, set_data=set_data)
    set_frame.pack(fill="both", expand=True)

    root.mainloop()
