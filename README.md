# Math2SQL

**Math2SQL** is a robust tool that automatically translates advanced mathematical expressions into SQL queries, supporting multiple database dialects. It bridges the gap between mathematical notation and database computation.

---

## Key Features

- **Advanced Mathematical Parsing**: Accurately parses complex formulas involving trigonometric functions, logarithms, exponentials, nested expressions, and more.
- **Multi-Dialect SQL Support**: Currently supports PostgreSQL and MySQL, with an architecture designed for easy expansion.
- **Instant Conversion**: Input a mathematical formula, select your SQL dialect, and receive the translated query instantly.
- **Clean Web Interface**: A minimalist and intuitive web UI for a smooth user experience and easy testing.
- **Extensible Architecture**: The core parsing logic is decoupled from the SQL conversion modules, making it straightforward to add support for new database dialects or mathematical functions.

---

## Project Structure

```
├── api/                # Flask backend API
│   ├── app.py          # Flask app initialization & config
│   └── routes.py       # API endpoint definitions
│
├── core/               # Core engine for parsing and conversion
│   ├── parser.py       # Mathematical expression parser (powered by Sympy)
│   ├── converter.py    # Base class for SQL converters
│   └── dialects/       # SQL dialect-specific converters
│       ├── postgresql.py
│       └── mysql.py
│
├── webapp/             # Frontend application
│   ├── templates/
│   │   └── index.html  # Main HTML page
│   └── static/         # For future CSS/JS files
│
├── .gitignore          # Git ignore rules
├── main.py             # Entry point for CLI (optional)
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

---

## Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/LeaderOnePro/math2sql.git
    cd math2sql
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Web Application**
    ```bash
    # Using the Flask CLI
    flask --app api.app run
    ```
    Alternatively, you can set the `FLASK_APP` environment variable first (`export FLASK_APP=api/app.py` or `$env:FLASK_APP="api/app.py"`) and then simply run `flask run`.

5.  **Access the Web Interface**
    Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Usage Example

- **Input Expression**: `sin(x)^2 + cos(y)^2`
- **Selected Dialect**: `PostgreSQL`
- **Generated SQL**:
  ```sql
  (POWER(SIN(x), 2) + POWER(COS(y), 2))
  ```

---

## Future Roadmap

-   Support for more advanced mathematical operations (e.g., integrals, derivatives, matrix operations).
-   Expansion of supported SQL dialects (e.g., SQL Server, Oracle, SQLite).
-   Implementation of intelligent variable and parameter management.
-   Comprehensive API documentation and an online demo.

---

## How to Contribute

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](<your-repo-url>/issues).

---

## License

This project is licensed under the MIT License.