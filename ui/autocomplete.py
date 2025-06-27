import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        self.suggestions_fetcher = kwargs.pop('suggestions_fetcher', lambda text: [])
        super().__init__(parent, *args, **kwargs)

        self.var = self["textvariable"]
        if not isinstance(self.var, tk.StringVar):
            self.var = tk.StringVar()
            self["textvariable"] = self.var

        self.var.trace('w', self.on_text_changed)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.selection)
        self.bind("<Escape>", self.hide_listbox)
        self.bind("<FocusOut>", self.hide_listbox)

        self.listbox_toplevel = None

    def on_text_changed(self, *args):
        if hasattr(self, '_debounce_id'):
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(300, self._perform_autocomplete)

    def _perform_autocomplete(self):
        text = self.var.get()
        if text:
            suggestions = self.suggestions_fetcher(text)
            if suggestions:
                self.show_listbox(suggestions)
            else:
                self.hide_listbox()
        else:
            self.hide_listbox()

    def show_listbox(self, suggestions):
        if not self.listbox_toplevel:
            x, y, _, h = self.bbox("insert")
            x += self.winfo_rootx()
            y += self.winfo_rooty() + h

            self.listbox_toplevel = tk.Toplevel(self)
            self.listbox_toplevel.wm_overrideredirect(True)
            self.listbox_toplevel.wm_geometry(f"+{x}+{y}")

            self.listbox = tk.Listbox(self.listbox_toplevel, width=self.cget("width"), exportselection=False,
                                      bg="#37474F", fg="#00BFFF", selectbackground="#42A5F5",
                                      selectforeground="white", borderwidth=0, highlightthickness=0)
            self.listbox.pack(side="left", fill="both", expand=True)
            self.listbox.bind("<<ListboxSelect>>", self.selection)
            self.listbox.bind("<Button-1>", self.selection) # Select on click
            
        self.listbox.delete(0, "end")
        for item in suggestions:
            self.listbox.insert("end", item)
        
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.listbox.see(0)
        else:
            self.hide_listbox()

    def hide_listbox(self, event=None):
        if self.listbox_toplevel:
            self.listbox_toplevel.destroy()
            self.listbox_toplevel = None

    def selection(self, event=None):
        if self.listbox_toplevel:
            try:
                if event and event.type == '4': # Button-1 click
                    selected_index = self.listbox.nearest(event.y)
                else:
                    selected_index = self.listbox.curselection()[0]
                
                value = self.listbox.get(selected_index)
                self.var.set(value)
                self.icursor("end")
            except (IndexError, tk.TclError):
                pass # No selection or widget destroyed
            self.hide_listbox()
            self.focus_set()
            return "break"

    def move_up(self, event):
        if self.listbox_toplevel and self.listbox.size() > 0:
            try:
                selected_index = self.listbox.curselection()[0]
                if selected_index > 0:
                    self.listbox.selection_clear(selected_index)
                    selected_index -= 1
                    self.listbox.selection_set(selected_index)
                    self.listbox.see(selected_index)
            except IndexError:
                self.listbox.selection_set(self.listbox.size() - 1)
                self.listbox.see(self.listbox.size() - 1)
            return "break"

    def move_down(self, event):
        if self.listbox_toplevel and self.listbox.size() > 0:
            try:
                selected_index = self.listbox.curselection()[0]
                if selected_index < self.listbox.size() - 1:
                    self.listbox.selection_clear(selected_index)
                    selected_index += 1
                    self.listbox.selection_set(selected_index)
                    self.listbox.see(selected_index)
            except IndexError:
                self.listbox.selection_set(0)
                self.listbox.see(0)
            return "break"
