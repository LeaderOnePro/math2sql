# API routes for math2sql

from flask import request, jsonify
from . import app # Assuming app is defined in api/__init__.py or app.py
from ..core.parser import MathParser
from ..core.dialects.postgresql import PostgreSQLConverter
from ..core.dialects.mysql import MySQLConverter
# Import other dialect converters as needed

parser = MathParser()
converters = {
    "postgresql": PostgreSQLConverter(),
    "mysql": MySQLConverter(),
    # Add other dialects here
}

@app.route('/convert', methods=['POST'])
def convert_math_to_sql():
    data = request.get_json()
    if not data or 'expression' not in data or 'dialect' not in data:
        return jsonify({'error': 'Missing expression or dialect in request'}), 400

    expression = data['expression']
    dialect = data['dialect'].lower()

    if dialect not in converters:
        return jsonify({'error': f'Unsupported SQL dialect: {dialect}'}), 400

    try:
        parsed_expression = parser.parse(expression)
        # In a real implementation, parsed_expression would be an AST or sympy object
        # For now, if parser.parse is a placeholder, we might pass the string directly
        # or a dummy parsed object.
        # This is a placeholder: actual parsing and conversion needed.
        if parsed_expression is None: # Assuming parser.parse returns something sympy can use
             # This is a temporary measure if parser.parse isn't implemented yet
             # We should ideally ensure parser.parse returns a usable structure
             # For now, we'll use a string representation for the converter placeholder
             parsed_expression = expression 

        sql_query = converters[dialect].convert(parsed_expression)
        return jsonify({'sql_query': sql_query})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Placeholder for a root or health check endpoint
@app.route('/')
def index():
    return jsonify({'message': 'Math2SQL API is running!'}) 