import tkinter as tk
from tkinter import ttk, simpledialog
from data.api import StarCitizenAPI
from ui.autocomplete import AutocompleteEntry

class JournalDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_values=None):
        self.initial_values = initial_values
        self.all_systems = StarCitizenAPI.get_all_systems()
        super().__init__(parent, title)

    def body(self, master):
        # Style the dialog background
        master.configure(background="#212121")

        ttk.Label(master, text="Title:").grid(row=0, sticky="w")
        self.title_entry = ttk.Entry(master, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="System:").grid(row=1, sticky="w")
        self.system_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=self.system_suggestions)
        self.system_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Planet:").grid(row=2, sticky="w")
        self.planet_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=StarCitizenAPI.search_locations)
        self.planet_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Notes:").grid(row=3, sticky="nw")
        self.notes_text = tk.Text(master, width=50, height=10, bg="#313131", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.notes_text.grid(row=3, column=1, padx=5, pady=5)

        if self.initial_values:
            self.title_entry.insert(0, self.initial_values.get('title', ''))
            self.system_entry.var.set(self.initial_values.get('system', ''))
            self.planet_entry.var.set(self.initial_values.get('planet', ''))
            self.notes_text.insert("1.0", self.initial_values.get('notes', ''))
        
        return self.title_entry # initial focus

    def system_suggestions(self, text):
        if not text:
            return []
        return [s for s in self.all_systems if text.lower() in s.lower()]

    def apply(self):
        self.result = {
            "title": self.title_entry.get(),
            "system": self.system_entry.get(),
            "planet": self.planet_entry.get(),
            "notes": self.notes_text.get("1.0", "end-1c")
        }

class SalvageDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_values=None):
        self.initial_values = initial_values
        self.all_systems = StarCitizenAPI.get_all_systems()
        super().__init__(parent, title)

    def body(self, master):
        master.configure(background="#212121")
        ttk.Label(master, text="System:").grid(row=0, sticky="w")
        self.system_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=self.system_suggestions)
        self.system_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Location:").grid(row=1, sticky="w")
        self.location_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=StarCitizenAPI.search_locations)
        self.location_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Ship Type:").grid(row=2, sticky="w")
        self.ship_type_entry = ttk.Entry(master, width=50)
        self.ship_type_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Salvage Details:").grid(row=3, sticky="nw")
        self.notes_text = tk.Text(master, width=50, height=10, bg="#313131", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.notes_text.grid(row=3, column=1, padx=5, pady=5)

        if self.initial_values:
            self.system_entry.var.set(self.initial_values.get('system', ''))
            self.location_entry.var.set(self.initial_values.get('location', ''))
            self.ship_type_entry.insert(0, self.initial_values.get('ship_type', ''))
            self.notes_text.insert("1.0", self.initial_values.get('notes', ''))
        
        return self.system_entry # initial focus

    def system_suggestions(self, text):
        if not text:
            return []
        return [s for s in self.all_systems if text.lower() in s.lower()]

    def apply(self):
        self.result = {
            "system": self.system_entry.get(),
            "location": self.location_entry.get(),
            "ship_type": self.ship_type_entry.get(),
            "notes": self.notes_text.get("1.0", "end-1c")
        }

class MiningDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_values=None):
        self.initial_values = initial_values
        self.all_systems = StarCitizenAPI.get_all_systems()
        super().__init__(parent, title)

    def body(self, master):
        master.configure(background="#212121")
        ttk.Label(master, text="System:").grid(row=0, sticky="w")
        self.system_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=self.system_suggestions)
        self.system_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Location Description:").grid(row=1, sticky="w")
        self.location_entry = AutocompleteEntry(master, width=50, suggestions_fetcher=StarCitizenAPI.search_locations)
        self.location_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Resource Type:").grid(row=2, sticky="w")
        self.resource_entry = ttk.Entry(master, width=50)
        self.resource_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Notes:").grid(row=3, sticky="nw")
        self.notes_text = tk.Text(master, width=50, height=10, bg="#313131", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.notes_text.grid(row=3, column=1, padx=5, pady=5)

        if self.initial_values:
            self.system_entry.var.set(self.initial_values.get('system', ''))
            self.location_entry.var.set(self.initial_values.get('location_description', ''))
            self.resource_entry.insert(0, self.initial_values.get('resource_type', ''))
            self.notes_text.insert("1.0", self.initial_values.get('notes', ''))

        return self.system_entry # initial focus

    def system_suggestions(self, text):
        if not text:
            return []
        return [s for s in self.all_systems if text.lower() in s.lower()]

    def apply(self):
        self.result = {
            "system": self.system_entry.get(),
            "location_description": self.location_entry.get(),
            "resource_type": self.resource_entry.get(),
            "notes": self.notes_text.get("1.0", "end-1c")
        }
