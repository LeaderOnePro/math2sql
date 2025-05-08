# API routes for math2sql

from flask import request, jsonify, render_template
# Ensure 'app' is imported correctly from the .app module (api/app.py)
from .app import app 
from core.parser import MathParser
from core.dialects.postgresql import PostgreSQLConverter
from core.dialects.mysql import MySQLConverter
# Import other dialect converters as needed

parser = MathParser()
converters = {
    "postgresql": PostgreSQLConverter(),
    "mysql": MySQLConverter(), # Placeholder, will need implementation
    # Add other dialects here
}

@app.route('/convert', methods=['POST'])
def convert_math_to_sql():
    data = request.get_json()
    if not data or 'expression' not in data or 'dialect' not in data:
        return jsonify({'error': '请求中缺少表达式或方言 (Missing expression or dialect in request)'}), 400

    expression = data['expression']
    dialect_name = data['dialect'].lower()

    if dialect_name not in converters:
        return jsonify({'error': f'不支持的SQL方言 (Unsupported SQL dialect): {dialect_name}'}), 400

    try:
        # MathParser.parse is expected to return a sympy expression or raise ValueError
        parsed_expression = parser.parse(expression)
        
        # Converters are expected to take the sympy expression and return a SQL string
        # or raise NotImplementedError for unsupported operations/functions.
        sql_query = converters[dialect_name].convert(parsed_expression)
        return jsonify({'sql_query': sql_query})
    
    except ValueError as e: # Errors from MathParser.parse()
        app.logger.warn(f"Parsing error for expression '{expression}': {e}")
        return jsonify({'error': f'数学表达式解析错误 (Parsing error): {str(e)}'}), 400
    except NotImplementedError as e: # Errors from converter.convert()
        app.logger.warn(f"Conversion not implemented for part of '{expression}' with dialect '{dialect_name}': {e}")
        return jsonify({'error': f'SQL转换错误 (Conversion error - not implemented): {str(e)}'}), 501 # 501 Not Implemented
    except Exception as e:
        # Catch-all for any other unexpected errors during parsing or conversion
        app.logger.error(f"Unexpected error converting expression '{expression}' for dialect '{dialect_name}': {e}", exc_info=True)
        return jsonify({'error': '服务器发生意外错误 (An unexpected error occurred on the server)'}), 500

@app.route('/')
def serve_index_page():
    """Serves the main index.html page."""
    return render_template('index.html')

# You might want an API status endpoint separately if needed.
# @app.route('/api/status')
# def api_status():
#    return jsonify({'message': 'Math2SQL API is running!'}) 