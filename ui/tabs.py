import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs import JournalDialog, SalvageDialog, MiningDialog

class JournalTab(ttk.Frame):
    def __init__(self, parent, journal):
        super().__init__(parent)
        self.journal = journal
        self.create_widgets()

    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.bind("<Return>", lambda event: self.refresh_journal_list())
        search_button = ttk.Button(search_frame, text="Search", command=self.refresh_journal_list)
        search_button.pack(side="left")
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")
        add_button = ttk.Button(button_frame, text="Add Entry", command=self.add_journal_entry_dialog)
        add_button.pack(side="left", padx=5)
        edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_journal_entry_dialog)
        edit_button.pack(side="left", padx=5)
        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_journal_entry)
        delete_button.pack(side="left", padx=5)
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side="left", fill="both", expand=True)
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        columns = ("id", "title", "system", "planet", "timestamp")
        self.journal_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.journal_tree.heading("id", text="ID")
        self.journal_tree.heading("title", text="Title")
        self.journal_tree.heading("system", text="System")
        self.journal_tree.heading("planet", text="Planet")
        self.journal_tree.heading("timestamp", text="Timestamp")
        self.journal_tree.column("id", width=50, stretch=tk.NO)
        self.journal_tree.column("title", width=150)
        self.journal_tree.column("system", width=100)
        self.journal_tree.column("planet", width=100)
        self.journal_tree.column("timestamp", width=150)
        self.journal_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.journal_tree.yview)
        self.journal_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        notes_label = ttk.Label(details_frame, text="Entry Notes:")
        notes_label.pack(anchor="w")
        self.journal_notes_text = tk.Text(details_frame, height=10, width=40, state="disabled", wrap="word", bg="#37474F", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.journal_notes_text.pack(fill="both", expand=True)
        self.journal_tree.bind("<<TreeviewSelect>>", self.show_journal_notes)
        self.refresh_journal_list()
    def refresh_journal_list(self):
        for item in self.journal_tree.get_children():
            self.journal_tree.delete(item)
        entries = self.journal.get_all_entries()
        search_term = self.search_var.get().lower()
        self.journal_data = {}
        for entry in entries:
            if not search_term or any(search_term in str(field).lower() for field in entry[1:5]):
                self.journal_data[entry[0]] = entry
                self.journal_tree.insert("", "end", iid=entry[0], values=(entry[0], entry[1], entry[2], entry[3], entry[5]))
    def show_journal_notes(self, event=None):
        selected_item = self.journal_tree.focus()
        if not selected_item:
            self.journal_notes_text.config(state="normal")
            self.journal_notes_text.delete("1.0", "end")
            self.journal_notes_text.config(state="disabled")
            return
        entry_data = self.journal_data.get(int(selected_item))
        if entry_data:
            notes = entry_data[4]
            self.journal_notes_text.config(state="normal")
            self.journal_notes_text.delete("1.0", "end")
            self.journal_notes_text.insert("1.0", notes)
            self.journal_notes_text.config(state="disabled")
    def add_journal_entry_dialog(self):
        dialog = JournalDialog(self, title="Add Journal Entry")
        if dialog.result:
            data = dialog.result
            self.journal.add_entry(data['title'], data['system'], data['planet'], data['notes'])
            self.refresh_journal_list()
            messagebox.showinfo("Success", "Journal entry added successfully.")
    def edit_journal_entry_dialog(self):
        selected_item = self.journal_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return
        entry_id = int(selected_item)
        entry_data = self.journal_data.get(entry_id)
        if not entry_data:
            messagebox.showerror("Error", "Could not find data for the selected entry.")
            return
        initial_values = {
            'title': entry_data[1],
            'system': entry_data[2],
            'planet': entry_data[3],
            'notes': entry_data[4]
        }
        dialog = JournalDialog(self, title="Edit Journal Entry", initial_values=initial_values)
        if dialog.result:
            data = dialog.result
            self.journal.update_entry(entry_id, data['title'], data['system'], data['planet'], data['notes'])
            self.refresh_journal_list()
            messagebox.showinfo("Success", "Journal entry updated successfully.")
    def delete_journal_entry(self):
        selected_item = self.journal_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            entry_id = int(selected_item)
            self.journal.delete_entry(entry_id)
            self.refresh_journal_list()
            self.show_journal_notes()
            messagebox.showinfo("Success", "Journal entry deleted successfully.")

class SalvageTab(ttk.Frame):
    def __init__(self, parent, journal):
        super().__init__(parent)
        self.journal = journal
        self.create_widgets()
    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.bind("<Return>", lambda event: self.refresh_salvage_list())
        search_button = ttk.Button(search_frame, text="Search", command=self.refresh_salvage_list)
        search_button.pack(side="left")
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")
        add_button = ttk.Button(button_frame, text="Add Wreck", command=self.add_salvage_wreck_dialog)
        add_button.pack(side="left", padx=5)
        edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_salvage_wreck_dialog)
        edit_button.pack(side="left", padx=5)
        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_salvage_wreck)
        delete_button.pack(side="left", padx=5)
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side="left", fill="both", expand=True)
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        columns = ("id", "system", "location", "ship_type", "timestamp")
        self.salvage_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.salvage_tree.heading("id", text="ID")
        self.salvage_tree.heading("system", text="System")
        self.salvage_tree.heading("location", text="Location")
        self.salvage_tree.heading("ship_type", text="Ship Type")
        self.salvage_tree.heading("timestamp", text="Timestamp")
        self.salvage_tree.column("id", width=50, stretch=tk.NO)
        self.salvage_tree.column("system", width=100)
        self.salvage_tree.column("location", width=200)
        self.salvage_tree.column("ship_type", width=100)
        self.salvage_tree.column("timestamp", width=150)
        self.salvage_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.salvage_tree.yview)
        self.salvage_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        notes_label = ttk.Label(details_frame, text="Salvage Details:")
        notes_label.pack(anchor="w")
        self.salvage_notes_text = tk.Text(details_frame, height=10, width=40, state="disabled", wrap="word", bg="#37474F", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.salvage_notes_text.pack(fill="both", expand=True)
        self.salvage_tree.bind("<<TreeviewSelect>>", self.show_salvage_notes)
        self.refresh_salvage_list()
    def refresh_salvage_list(self):
        for item in self.salvage_tree.get_children():
            self.salvage_tree.delete(item)
        wrecks = self.journal.get_all_salvage_wrecks()
        search_term = self.search_var.get().lower()
        self.salvage_data = {}
        for wreck in wrecks:
            if not search_term or any(search_term in str(field).lower() for field in wreck[1:5]):
                self.salvage_data[wreck[0]] = wreck
                self.salvage_tree.insert("", "end", iid=wreck[0], values=(wreck[0], wreck[1], wreck[2], wreck[3], wreck[5]))
    def show_salvage_notes(self, event=None):
        selected_item = self.salvage_tree.focus()
        if not selected_item:
            self.salvage_notes_text.config(state="normal")
            self.salvage_notes_text.delete("1.0", "end")
            self.salvage_notes_text.config(state="disabled")
            return
        wreck_data = self.salvage_data.get(int(selected_item))
        if wreck_data:
            notes = wreck_data[4]
            self.salvage_notes_text.config(state="normal")
            self.salvage_notes_text.delete("1.0", "end")
            self.salvage_notes_text.insert("1.0", notes)
            self.salvage_notes_text.config(state="disabled")
    def add_salvage_wreck_dialog(self):
        dialog = SalvageDialog(self, title="Add Salvage Wreck")
        if dialog.result:
            data = dialog.result
            self.journal.add_salvage_wreck(data['system'], data['location'], data['ship_type'], data['notes'])
            self.refresh_salvage_list()
            messagebox.showinfo("Success", "Salvage wreck added successfully.")
    def edit_salvage_wreck_dialog(self):
        selected_item = self.salvage_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a wreck to edit.")
            return
        wreck_id = int(selected_item)
        wreck_data = self.salvage_data.get(wreck_id)
        if not wreck_data:
            messagebox.showerror("Error", "Could not find data for the selected wreck.")
            return
        initial_values = {
            'system': wreck_data[1],
            'location': wreck_data[2],
            'ship_type': wreck_data[3],
            'notes': wreck_data[4]
        }
        dialog = SalvageDialog(self, title="Edit Salvage Wreck", initial_values=initial_values)
        if dialog.result:
            data = dialog.result
            self.journal.update_salvage_wreck(wreck_id, data['system'], data['location'], data['ship_type'], data['notes'])
            self.refresh_salvage_list()
            messagebox.showinfo("Success", "Salvage wreck updated successfully.")
    def delete_salvage_wreck(self):
        selected_item = self.salvage_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a wreck to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected wreck?"):
            wreck_id = int(selected_item)
            self.journal.delete_salvage_wreck(wreck_id)
            self.refresh_salvage_list()
            self.show_salvage_notes()
            messagebox.showinfo("Success", "Salvage wreck deleted successfully.")

class MiningTab(ttk.Frame):
    def __init__(self, parent, journal):
        super().__init__(parent)
        self.journal = journal
        self.create_widgets()
    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.bind("<Return>", lambda event: self.refresh_mining_list())
        search_button = ttk.Button(search_frame, text="Search", command=self.refresh_mining_list)
        search_button.pack(side="left")
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")
        add_button = ttk.Button(button_frame, text="Add Location", command=self.add_mining_location_dialog)
        add_button.pack(side="left", padx=5)
        edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_mining_location_dialog)
        edit_button.pack(side="left", padx=5)
        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_mining_location)
        delete_button.pack(side="left", padx=5)
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side="left", fill="both", expand=True)
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        columns = ("id", "system", "location", "resource", "timestamp")
        self.mining_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.mining_tree.heading("id", text="ID")
        self.mining_tree.heading("system", text="System")
        self.mining_tree.heading("location", text="Location")
        self.mining_tree.heading("resource", text="Resource")
        self.mining_tree.heading("timestamp", text="Timestamp")
        self.mining_tree.column("id", width=50, stretch=tk.NO)
        self.mining_tree.column("system", width=100)
        self.mining_tree.column("location", width=150)
        self.mining_tree.column("resource", width=100)
        self.mining_tree.column("timestamp", width=150)
        self.mining_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.mining_tree.yview)
        self.mining_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        notes_label = ttk.Label(details_frame, text="Mining Notes:")
        notes_label.pack(anchor="w")
        self.mining_notes_text = tk.Text(details_frame, height=10, width=40, state="disabled", wrap="word", bg="#37474F", fg="#00BFFF", insertbackground="white", selectbackground="#42A5F5", selectforeground="white", borderwidth=0, highlightthickness=0)
        self.mining_notes_text.pack(fill="both", expand=True)
        self.mining_tree.bind("<<TreeviewSelect>>", self.show_mining_notes)
        self.refresh_mining_list()
    def refresh_mining_list(self):
        for item in self.mining_tree.get_children():
            self.mining_tree.delete(item)
        locations = self.journal.get_all_mining_locations()
        search_term = self.search_var.get().lower()
        self.mining_data = {}
        for location in locations:
            if not search_term or any(search_term in str(field).lower() for field in location[1:5]):
                self.mining_data[location[0]] = location
                self.mining_tree.insert("", "end", iid=location[0], values=(location[0], location[1], location[2], location[3], location[5]))
    def show_mining_notes(self, event=None):
        selected_item = self.mining_tree.focus()
        if not selected_item:
            self.mining_notes_text.config(state="normal")
            self.mining_notes_text.delete("1.0", "end")
            self.mining_notes_text.config(state="disabled")
            return
        loc_data = self.mining_data.get(int(selected_item))
        if loc_data:
            notes = loc_data[4]
            self.mining_notes_text.config(state="normal")
            self.mining_notes_text.delete("1.0", "end")
            self.mining_notes_text.insert("1.0", notes)
            self.mining_notes_text.config(state="disabled")
    def add_mining_location_dialog(self):
        dialog = MiningDialog(self, title="Add Mining Location")
        if dialog.result:
            data = dialog.result
            self.journal.add_mining_location(data['system'], data['location_description'], data['resource_type'], data['notes'])
            self.refresh_mining_list()
            messagebox.showinfo("Success", "Mining location added successfully.")
    def edit_mining_location_dialog(self):
        selected_item = self.mining_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a location to edit.")
            return
        loc_id = int(selected_item)
        loc_data = self.mining_data.get(loc_id)
        if not loc_data:
            messagebox.showerror("Error", "Could not find data for the selected location.")
            return
        initial_values = {
            'system': loc_data[1],
            'location_description': loc_data[2],
            'resource_type': loc_data[3],
            'notes': loc_data[4]
        }
        dialog = MiningDialog(self, title="Edit Mining Location", initial_values=initial_values)
        if dialog.result:
            data = dialog.result
            self.journal.update_mining_location(loc_id, data['system'], data['location_description'], data['resource_type'], data['notes'])
            self.refresh_mining_list()
            messagebox.showinfo("Success", "Mining location updated successfully.")
    def delete_mining_location(self):
        selected_item = self.mining_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a location to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected location?"):
            loc_id = int(selected_item)
            self.journal.delete_mining_location(loc_id)
            self.refresh_mining_list()
            self.show_mining_notes()
            messagebox.showinfo("Success", "Mining location deleted successfully.")
