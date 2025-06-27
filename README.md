# Star Citizen Helper - Datapad

> A personal datapad for tracking your adventures in the 'verse.

This desktop application serves as a personal journal and datapad for players of the game Star Citizen. It allows you to log important information, such as general discoveries, valuable salvage wreck locations, and rich mining spots, so you never lose track of them. The application integrates with the [Star Citizen Tools API](https://scit.tools/) to provide in-game context and data, like system and planet names.

*(Suggestion: Add a screenshot of the application here once you are happy with the final look!)*
`![App Screenshot](placeholder.png)`

## About The Project

This tool was built to provide a simple, offline-first way to manage personal points of interest within Star Citizen. Whether you're a trader, explorer, salvager, or miner, this datapad helps you organize your findings efficiently.

### Key Features

*   **Multi-Category Journaling**: Separate tabs for general entries, salvage wrecks, and mining locations.
*   **Detailed Entries**: Store crucial details for each entry, including system, location, notes, and relevant metadata.
*   **Live Game Data**: Autocompletes system and celestial object names using the Star Citizen Tools API.
*   **Location Details**: Fetches and displays descriptions and types for known celestial objects.
*   **Search Functionality**: Quickly find any entry across all categories.
*   **Persistent Storage**: Your data is stored locally in a SQLite database file (`starcitizen_journal.db`).
*   **Themed Interface**: A clean, dark-themed UI built with Python's native Tkinter library.

### Built With

*   [Python](https://www.python.org/)
*   [Tkinter](https://docs.python.org/3/library/tkinter.html)
*   [SQLite](https://www.sqlite.org/index.html)
*   [Requests](https://requests.readthedocs.io/en/latest/)

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Ensure you have Python 3 and pip installed on your system.

*   **Python**
*   **pip**

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your_username/your_repository_name.git
    cd your_repository_name
    ```
2.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application from the project's root directory:
    ```sh
    python main.py
    ```
2.  The application window will open, and a `starcitizen_journal.db` file will be automatically created in the root directory to store your data.
3.  Use the tabs to navigate between categories and the buttons to add, edit, or delete your entries.

## Acknowledgements

*   **Star Citizen Tools API** by [SCIT](https://scit.tools/) for providing the starmap and location data.
*   **SC Trade Tools API** for their excellent and easy-to-use trade data endpoints.
*   The awesome community at [r/starcitizen](https://www.reddit.com/r/starcitizen/) for the inspiration.
