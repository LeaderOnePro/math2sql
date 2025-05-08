# Main script for command-line usage or direct testing

from core.parser import MathParser
from core.dialects.postgresql import PostgreSQLConverter
from core.dialects.mysql import MySQLConverter

def main():
    parser = MathParser()
    # Example usage:
    # expression_str = "sin(x)^2 + cos(x)^2"
    # print(f"Original expression: {expression_str}")

    # parsed_expr = parser.parse(expression_str) # This will be a sympy object if implemented

    # pg_converter = PostgreSQLConverter()
    # try:
    #     # Note: The convert method expects a parsed sympy expression, 
    #     # not a raw string, once fully implemented.
    #     # For now, placeholders might accept strings for basic demonstration.
    #     pg_sql = pg_converter.convert(expression_str) # Adjust based on actual parser output
    #     print(f"PostgreSQL: {pg_sql}")
    # except Exception as e:
    #     print(f"Error converting to PostgreSQL: {e}")

    # mysql_converter = MySQLConverter()
    # try:
    #     mysql_sql = mysql_converter.convert(expression_str) # Adjust as above
    #     print(f"MySQL: {mysql_sql}")
    # except Exception as e:
    #     print(f"Error converting to MySQL: {e}")
    
    print("Math2SQL CLI - (Add command line argument parsing here)")
    print("Example: python main.py \"your_math_expression_here\" --dialect postgresql")
    # TODO: Implement argument parsing (e.g., using argparse)
    # to take math expression and dialect from command line.

if __name__ == "__main__":
    main() 