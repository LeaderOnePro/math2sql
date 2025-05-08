# Math2SQL

Converts mathematical expressions into SQL queries for various SQL dialects.

## Project Goal

Inspired by a tweet showcasing math operations in Postgres, this tool aims to provide a more general solution for translating mathematical formulas (including those from higher mathematics) into SQL.

## Features (Planned)

-   Parse complex mathematical expressions.
-   Support for common mathematical functions (trigonometric, logarithmic, exponential, etc.).
-   Support for advanced mathematical concepts (e.g., derivatives, integrals - ambitious goal).
-   Output SQL for multiple dialects (PostgreSQL, MySQL, potentially others like SQL Server, Oracle, SQLite).
-   Web interface for easy conversion.
-   Command-line interface for scripting and batch processing.

## Project Structure

-   `core/`: Core parsing and conversion logic.
    -   `parser.py`: Mathematical expression parser (likely using Sympy).
    -   `converter.py`: Base class for SQL conversion.
    -   `dialects/`: Specific SQL dialect converters.
-   `api/`: Flask-based web API.
    -   `app.py`: Flask app setup.
    -   `routes.py`: API endpoints.
-   `webapp/`: Frontend (HTML, CSS, JS).
    -   `templates/index.html`: Main web page.
    -   `static/`: For CSS and JS files.
-   `main.py`: CLI entry point.
-   `requirements.txt`: Python dependencies.

## Setup and Running

(Instructions to be added once the core functionality is in place)

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run the Flask app (example):
    ```bash
    # Ensure your PYTHONPATH is set up if running from outside the api directory, or cd into it
    # export PYTHONPATH=..
    # For Flask 2.x and later, if app.py is in api/
    flask --app api.app run 
    # If your main flask app object is named 'app' within api/app.py, then you can do:
    # cd api
    # flask run
    # Or from root, if FLASK_APP is set to api/app.py
    ```
    (More specific instructions for running will be refined)

## How to Contribute

(Guidelines to be added) 