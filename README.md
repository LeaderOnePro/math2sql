# Math2SQL

Converts mathematical expressions into SQL queries for various SQL dialects.

## Project Goal

Inspired by a tweet showcasing math operations in Postgres, this tool aims to provide a more general solution for translating mathematical formulas (including those from higher mathematics) into SQL.

## Current Features

- Basic Flask API structure (`api/app.py`, `api/routes.py`).
- Core structure for mathematical expression parsing and SQL conversion (`core/parser.py`, `core/converter.py`).
- Initial dialect support for MySQL and PostgreSQL (`core/dialects/mysql.py`, `core/dialects/postgresql.py`).
- Basic web interface template (`webapp/templates/index.html`).

## Features (Planned)

-   Implement robust parsing of complex mathematical expressions.
-   Add support for a wide range of common mathematical functions (trigonometric, logarithmic, exponential, etc.).
-   Explore support for advanced mathematical concepts (e.g., derivatives, integrals - ambitious goal).
-   Expand SQL dialect support (e.g., SQL Server, Oracle, SQLite).
-   Develop a functional web interface for easy conversion.
-   Implement a command-line interface for scripting and batch processing.

## Project Structure

-   `core/`: Core parsing and conversion logic.
    -   `parser.py`: Mathematical expression parser.
    -   `converter.py`: Base class for SQL conversion.
    -   `dialects/`: Specific SQL dialect converters (`mysql.py`, `postgresql.py`).
-   `api/`: Flask-based web API.
    -   `app.py`: Flask app setup.
    -   `routes.py`: API endpoints.
-   `webapp/`: Frontend.
    -   `templates/index.html`: Main web page for the application.
-   `main.py`: Potential CLI entry point (currently not implemented).
-   `requirements.txt`: Python dependencies.
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
-   `README.md`: This file.

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LeaderOnePro/math2sql.git
    cd math2sql
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    ```
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask application (Development Server):**
    From the project root directory (`math2sql/`):
    ```bash
    # Set the FLASK_APP environment variable
    # On Windows (PowerShell)
    $env:FLASK_APP = "api.app"
    # On Windows (Command Prompt)
    set FLASK_APP=api.app
    # On macOS/Linux
    export FLASK_APP=api.app

    # Set FLASK_DEBUG for development mode (optional, enables auto-reloading and debugger)
    # On Windows (PowerShell)
    $env:FLASK_DEBUG = "1"
    # On Windows (Command Prompt)
    set FLASK_DEBUG=1
    # On macOS/Linux
    export FLASK_DEBUG=1

    # Run the Flask app
    flask run
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

    Alternatively, you can directly run `api/app.py` if it's structured to start the server:
    ```bash
    python api/app.py
    ```
    (Ensure `app.run()` is called within `api/app.py` for this method to work.)

## How to Contribute

(Guidelines to be added)