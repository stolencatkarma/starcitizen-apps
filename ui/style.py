from tkinter import ttk

def setup_style(style):
    BG_COLOR = "#212121"  # Dark grey
    FG_COLOR = "#00BFFF"  # Deep Sky Blue
    ACCENT_COLOR = "#42A5F5"  # A lighter blue for accents
    INACTIVE_FG_COLOR = "#B0BEC5" # Grey for inactive tabs
    TEXT_BG = "#37474F" # Slightly lighter grey for text entry
    FONT_FAMILY = "Consolas"
    FONT_SIZE = 10

    style.theme_use('clam')

    # General widget styling
    style.configure('.',
                    background=BG_COLOR,
                    foreground=FG_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE),
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor='')

    # Frame and Label
    style.configure("TFrame", background=BG_COLOR)
    style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, padding=5)
    
    # Button
    style.configure("TButton",
                    background=ACCENT_COLOR,
                    foreground="#FFFFFF",
                    font=(FONT_FAMILY, FONT_SIZE, "bold"),
                    padding=8,
                    borderwidth=0)
    style.map("TButton",
            background=[('active', FG_COLOR)],
            foreground=[('active', BG_COLOR)])

    # Notebook
    style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=BG_COLOR,
                    foreground=INACTIVE_FG_COLOR,
                    padding=[12, 6],
                    font=(FONT_FAMILY, FONT_SIZE, "bold"),
                    borderwidth=0)
    style.map("TNotebook.Tab",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", "#FFFFFF")])

    # Treeview
    style.configure("Treeview",
                    background=TEXT_BG,
                    foreground=FG_COLOR,
                    fieldbackground=TEXT_BG,
                    rowheight=28,
                    borderwidth=0)
    style.map("Treeview",
            background=[('selected', ACCENT_COLOR)],
            foreground=[('selected', "#FFFFFF")])
    style.configure("Treeview.Heading",
                    background=BG_COLOR,
                    foreground=FG_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE + 1, "bold"),
                    padding=8)
    
    # Scrollbar
    style.configure("Vertical.TScrollbar",
                    gripcount=0,
                    background=ACCENT_COLOR,
                    darkcolor=TEXT_BG,
                    lightcolor=TEXT_BG,
                    troughcolor=BG_COLOR,
                    bordercolor=BG_COLOR,
                    arrowcolor="#FFFFFF")
    style.map("Vertical.TScrollbar",
              background=[('active', FG_COLOR)])
