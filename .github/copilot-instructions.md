# Star Citizen Helper - Datapad Recreation Guide

This document provides instructions for recreating the "Star Citizen Helper - Datapad" application using natural language prompts.

## 1. Project Setup

**Goal:** Initialize the project structure, install dependencies, and set up the main application window.

**Prompt:**

```
Create a new Python project for a Star Citizen journaling application.

1.  **Create the main application file `main.py`:** This file will contain the main application class and entry point.
2.  **Set up the UI structure:**
    *   Create a `ui` directory.
    *   Inside `ui`, create the following files:
        *   `tabs.py`: For the different tabs in the application (Journal, Salvage, Mining).
        *   `dialogs.py`: For the dialog boxes used to add and edit entries.
        *   `style.py`: For the application's visual styling.
        *   `autocomplete.py`: For the autocomplete entry widget.
3.  **Set up the data handling:**
    *   Create a `data` directory.
    *   Inside `data`, create the following files:
        *   `database.py`: To manage the SQLite database for storing journal entries.
        *   `api.py`: To interact with the Star Citizen Tools API for game data.
4.  **Install dependencies:**
    *   Create a `requirements.txt` file.
    *   Add the `requests` library to `requirements.txt`.
    *   Install the dependencies from `requirements.txt`.
5.  **Create the main application window in `main.py`:**
    *   Use the `tkinter` library.
    *   The main window should be an instance of a class named `App`.
    *   Set the title to "Star Citizen Helper - Datapad" and the initial size to 900x700.
    *   The `App` class should initialize a `Journal` object from `database.py`.
    *   The main window should have a dark theme.
```

## 2. Database Implementation

**Goal:** Implement the `Journal` class in `data/database.py` to handle all database operations.

**Prompt:**

```
In `data/database.py`, create a `Journal` class with the following features:

1.  **Initialization:**
    *   The `__init__` method should take a database file path as an argument and connect to the SQLite database.
    *   Call methods to create the necessary tables if they don't exist.
2.  **Table Creation:**
    *   Create three tables:
        *   `entries`: For general journal entries (id, title, system, planet, notes, timestamp).
        *   `salvage_wrecks`: For salvage locations (id, system, location_description, ship_type, notes, timestamp).
        *   `mining_locations`: For mining locations (id, system, location_description, resource_type, notes, timestamp).
3.  **CRUD Operations:**
    *   For each of the three tables, implement methods for:
        *   Adding a new record.
        *   Retrieving all records.
        *   Updating an existing record.
        *   Deleting a record.
```

## 3. API Integration

**Goal:** Implement the `StarCitizenAPI` class in `data/api.py` to fetch data from the Star Citizen Tools API.

**Prompt:**

```
In `data/api.py`, create a `StarCitizenAPI` class with the following static methods:

1.  **`get_all_systems()`:**
    *   Fetch all star systems from `https://api.scit.tools/v1/starmap/systems`.
    *   Cache the results to avoid repeated API calls.
2.  **`search_locations(query)`:**
    *   Search for locations (systems, celestial objects, points of interest) using the `https://api.scit.tools/v1/starmap/search` endpoint.
3.  **`get_location_details(location_name)`:**
    *   Fetch detailed information about a specific location by first searching for it to get its code, and then using the `https://api.scit.tools/v1/starmap/object` endpoint.
    *   Format the details into a human-readable string.
```

## 4. UI Implementation

### 4.1. Styling

**Goal:** Define the visual style of the application in `ui/style.py`.

**Prompt:**

```
In `ui/style.py`, create a function `setup_style(style)` that configures the `ttk.Style` for the application.

*   Use a dark theme with a color scheme of your choice (e.g., dark grey background, blue accents).
*   Define styles for the following widgets:
    *   `TNotebook` and `TNotebook.Tab`
    *   `TFrame`
    *   `TLabel`
    *   `TButton`
    *   `Treeview` and `Treeview.Heading`
    *   `Vertical.TScrollbar`
*   Use a monospaced font like "Consolas".
```

### 4.2. Autocomplete Entry

**Goal:** Create a reusable autocomplete entry widget in `ui/autocomplete.py`.

**Prompt:**

```
In `ui/autocomplete.py`, create a class `AutocompleteEntry` that inherits from `ttk.Entry`.

*   It should take a `suggestions_fetcher` function as an argument, which will be called to get a list of suggestions based on the user's input.
*   Show a listbox with suggestions when the user types.
*   Allow the user to navigate the suggestions using the up and down arrow keys and select an item with the Enter key or a mouse click.
*   Hide the listbox when the widget loses focus or the user presses Escape.
*   Use a debounce mechanism to avoid making too many calls to the `suggestions_fetcher` function.
```

### 4.3. Dialogs

**Goal:** Create the dialog boxes for adding and editing entries in `ui/dialogs.py`.

**Prompt:**

```
In `ui/dialogs.py`, create the following dialog classes that inherit from `tkinter.simpledialog.Dialog`:

1.  **`JournalDialog`:**
    *   Fields for Title, System, Planet, and Notes.
    *   Use the `AutocompleteEntry` for the System and Planet fields.
2.  **`SalvageDialog`:**
    *   Fields for System, Location, Ship Type, and Salvage Details.
    *   Use the `AutocompleteEntry` for the System and Location fields.
3.  **`MiningDialog`:**
    *   Fields for System, Location Description, Resource Type, and Notes.
    *   Use the `AutocompleteEntry` for the System and Location Description fields.

Each dialog should:
*   Take an optional `initial_values` dictionary to pre-fill the fields for editing.
*   Return the entered data as a dictionary.
*   Have a dark theme consistent with the main application.
```

### 4.4. Tabs

**Goal:** Create the main UI tabs in `ui/tabs.py`.

**Prompt:**

```
In `ui/tabs.py`, create the following classes that inherit from `ttk.Frame`:

1.  **`JournalTab`**
2.  **`SalvageTab`**
3.  **`MiningTab`**

Each tab class should:
*   Have a `Treeview` widget to display the list of entries.
*   Have buttons for adding, editing, and deleting entries.
*   Have a search bar to filter the list of entries.
*   Display the notes and other details of the selected entry in a `Text` widget.
*   For the `JournalTab`, `SalvageTab`, and `MiningTab`, also display the location details fetched from the `StarCitizenAPI`.
*   Implement the logic for refreshing the list, showing details, and handling the add, edit, and delete operations by calling the appropriate methods from the `Journal` class and showing the corresponding dialogs.
```

## 5. Final Assembly

**Goal:** Bring all the components together in `main.py`.

**Prompt:**

```
In `main.py`, update the `App` class to:

1.  Create a `ttk.Notebook` widget.
2.  Create instances of `JournalTab`, `SalvageTab`, and `MiningTab`.
3.  Add the tabs to the notebook.
4.  Set up the application's closing behavior.
5.  In the main execution block, create an instance of the `Journal` class and the `App` class, and start the main loop.
```