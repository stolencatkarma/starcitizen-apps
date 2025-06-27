import tkinter as tk
from tkinter import ttk
from data.database import Journal
from data.api import StarCitizenAPI
from ui.style import setup_style
from ui.tabs import JournalTab, SalvageTab, MiningTab

class App(tk.Tk):
    def __init__(self, journal):
        super().__init__()
        self.title("Star Citizen Helper - Datapad")
        self.geometry("900x700")
        self.journal = journal
        self.systems = StarCitizenAPI.get_all_systems()

        # --- Style Setup ---
        self.configure(background="#212121")
        style = ttk.Style(self)
        setup_style(style)
        # --- End Style Setup ---

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Create frames for each tab
        self.journal_tab = JournalTab(self.notebook, self.journal)
        self.salvage_tab = SalvageTab(self.notebook, self.journal)
        self.mining_tab = MiningTab(self.notebook, self.journal)

        self.notebook.add(self.journal_tab, text="Journal Entries")
        self.notebook.add(self.salvage_tab, text="Salvage Wrecks")
        self.notebook.add(self.mining_tab, text="Mining Locations")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    db_file = "starcitizen_journal.db"
    journal = Journal(db_file)
    app = App(journal)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()