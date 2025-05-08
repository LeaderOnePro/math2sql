# PostgreSQL specific conversion logic
from ..converter import BaseSQLConverter
import sympy

class PostgreSQLConverter(BaseSQLConverter):
    def __init__(self):
        self.function_map = {
            sympy.sin: "SIN",
            sympy.cos: "COS",
            sympy.tan: "TAN",
            sympy.asin: "ASIN",
            sympy.acos: "ACOS",
            sympy.atan: "ATAN",
            sympy.exp: "EXP",
            sympy.log: "LN",
            sympy.sqrt: "SQRT",
            sympy.Abs: "ABS",
        }

    def convert(self, expr):
        if isinstance(expr, sympy.Number):
            return str(expr)

        if isinstance(expr, sympy.Symbol):
            return str(expr)

        if isinstance(expr, sympy.Pow):
            base = self.convert(expr.base)
            exponent = self.convert(expr.exp)
            # PostgreSQL POWER function
            return f"POWER({base}, {exponent})"

        if isinstance(expr, sympy.Add):
            # Ensure correct precedence with parentheses for all terms being added/subtracted
            # Especially important if a term is negative, e.g., POWER(x, 2) + (-y)
            converted_args = []
            for arg in expr.args:
                c_arg = self.convert(arg)
                # if isinstance(arg, sympy.Number) and arg < 0: # Already handled by sympy's Mul representation for -y as -1*y
                #    converted_args.append(f"({c_arg})") 
                # else:
                converted_args.append(c_arg)
            return f"({' + '.join(converted_args)})".replace("+ -", "- ") # Basic handling for x + (-y)

        if isinstance(expr, sympy.Mul):
            # Handle division: x/y is represented as x * Pow(y, -1)
            # Or more generally, terms with negative exponents.
            numerator_terms = []
            denominator_terms = []
            
            # Separate negative one for unary minus if it's the only multiplier of that kind
            # e.g. -x -> Mul(-1, x) or -(x*y) -> Mul(-1, x, y)
            has_negative_one_multiplier = False
            processed_args = list(expr.args)

            if sympy.S.NegativeOne in processed_args:
                # Check if -1 is acting as a unary minus for the whole expression or part of it
                # This logic can get complex if -1 is mixed with other numbers.
                # For now, a simple check: if -1 is present, assume it makes the term negative.
                # More robust: count occurrences or check if it's the leading factor of a sub-expression.
                # Let's assume for now if -1 is an arg, the whole term is negative if not cancelled out.
                
                # Simplified: if -1 is present and not cancelled by another -1 (which sympy simplifies)
                # it acts as a negation for the product of other terms.
                # Example: -x*y -> Mul(-1, x, y).  (-x)*(-y) -> Mul(x,y) (sympy simplifies)
                
                # We'll try to pull out a single -1 if it exists to form a leading negative sign
                # This is tricky because sympy might have Mul(-1, Pow(y,-1)) for -1/y
                pass # Let the division logic handle Pow(y,-1) and Pow(x,-1) etc.

            for arg in expr.args:
                if isinstance(arg, sympy.Pow) and arg.exp.is_negative:
                    if arg.exp == -1:
                        denominator_terms.append(self.convert(arg.base))
                    else: # e.g., y**-2  becomes 1 / POWER(y,2)
                        denominator_terms.append(f"POWER({self.convert(arg.base)}, {self.convert(sympy.Abs(arg.exp))})")
                elif arg == sympy.S.NegativeOne and not numerator_terms and not denominator_terms and len(expr.args) > 1:
                    # Special case for leading -1 in a product that isn't just -1 itself.
                    # e.g. -x -> Mul(-1, x). We want to produce "-(x)"
                    # This is tricky because this -1 should apply to the *whole* product of remaining args.
                    # For now, we will let it be part of numerator_terms and handle negation later if possible,
                    # or rely on the + - replacement in Add.
                    numerator_terms.append("-1") 
                else:
                    numerator_terms.append(self.convert(arg))
            
            num_str = "1"
            if numerator_terms:
                # If -1 is a term, and it's the only one, it's just -1.
                # If it's with others, it's a multiplication.
                if "-1" in numerator_terms and len(numerator_terms) > 1:
                    # Try to make it a leading negation if it makes sense
                    # e.g., Mul(-1, x, y) -> -(x * y)
                    # Mul(-1, 2, x) -> -(2 * x)
                    # This is still hard to get right universally here.
                    # Simplest is to just multiply by -1.
                     idx = numerator_terms.index("-1")
                     # If -1 is present, and it's not the *only* term, form a negative product.
                     # This assumes other terms are positive or handled.
                     # This is a bit of a heuristic.
                     is_negative_product = True
                     numerator_terms.pop(idx)
                     if not numerator_terms: # only -1 was there (e.g. -1/y)
                         num_str = "-1"
                     else:
                         num_str = " * ".join(f"({t})" for t in numerator_terms)
                         num_str = f"-({num_str})" # Apply negation to the product of remaining terms
                elif numerator_terms == ["-1"]:
                    num_str = "-1"
                else:
                    num_str = " * ".join(f"({t})" for t in numerator_terms)
            
            if denominator_terms:
                den_str = " * ".join(f"({t})" for t in denominator_terms)
                # If numerator was just "1" and it became negative, it's "-1"
                if num_str == "-(1)": num_str = "-1" 
                elif num_str == "1" and den_str.startswith("-") : # e.g. 1 / (-y)
                     # This case is complex, better to keep denominator as is and let SQL handle 1 / (-val)
                     pass # den_str = den_str[2:-1]; num_str = f"-({num_str})" 

                # Ensure division by zero is not implicitly created if num_str is empty but becomes 1
                if not numerator_terms and num_str == "1" and not denominator_terms:
                    return "1" # Or handle as error if original expr was Mul() e.g. empty product
                
                return f"(CAST({num_str} AS DECIMAL) / {den_str})" # Using CAST for potentially better precision in division
            else:
                # If it was Mul(-1, x), num_str would be -(x). If just Mul(x,y), then (x)*(y)
                return num_str

        if isinstance(expr, sympy.Function):
            func_name = self.function_map.get(expr.func)
            if func_name:
                args_converted = [self.convert(arg) for arg in expr.args]
                return f"{func_name}({', '.join(args_converted)})"
            else:
                sympy_func_name_str = str(expr.func)
                # Handle specific sympy constructs that don't map directly to simple SQL functions
                if expr.func == sympy.Derivative:
                    # For Derivative(expr, var1, count1, var2, count2 ...)
                    # SQL doesn't have a generic derivative function. This would require symbolic pre-computation.
                    # Or, if the intent is to store the *expression* of the derivative, that's different.
                    raise NotImplementedError("Direct SQL conversion for symbolic Derivative is not supported. Pre-calculate the derivative first.")
                if expr.func == sympy.Integral:
                    raise NotImplementedError("Direct SQL conversion for symbolic Integral is not supported. Pre-calculate the integral first.")
                # Could add specific handling for other Sympy objects like Matrix, etc.
                # For unknown functions, error out rather than guessing a name
                raise NotImplementedError(f"SQL function for Sympy function '{sympy_func_name_str}' is not defined in function_map.")

        raise NotImplementedError(f"SQL conversion for expression type '{type(expr)}' (value: {expr}) is not yet implemented.")

if __name__ == '__main__':
    from ..core.parser import MathParser
    
    parser = MathParser()
    converter = PostgreSQLConverter()

    expressions_to_test = [
        "x + y - z",
        "x * y / z",
        "-x",
        "-x*y",
        "x*(-y)",
        "1/x",
        "-1/x",
        "x / (-y)",
        "sin(x)",
        "cos(y)^2",
        "ln(x^2 + 1)",
        "exp(-y^2)",
        "sqrt(abs(tan(x*y)) + 1)",
        "(sin(x) + cos(y))^2",
        "1 / (1 + ln(x^2 + 1))",
        "(sin(x) + cos(y))^2 / (1 + ln(x^2 + 1))",
        "(sin(x) + cos(y))^2 / (1 + ln(power(x,2) + 1)) + exp(-power(y,2)) * sqrt(abs(tan(x*y)) + 1)", # Full original example slightly modified for direct sympy parsing
        "x**-2", # Should be 1 / POWER(x,2)
        "1/x + 1/y",
        "-sqrt(x)"
    ]

    for expr_str in expressions_to_test:
        print(f"\nOriginal: {expr_str}")
        try:
            parsed_expr = parser.parse(expr_str)
            print(f"Sympy expr: {parsed_expr} (type: {type(parsed_expr)})")
            # For Mul, show args: if isinstance(parsed_expr, sympy.Mul): print(f"  Mul args: {parsed_expr.args}")
            # For Add, show args: if isinstance(parsed_expr, sympy.Add): print(f"  Add args: {parsed_expr.args}")
            # For Pow, show base/exp: if isinstance(parsed_expr, sympy.Pow): print(f"  Pow base: {parsed_expr.base}, exp: {parsed_expr.exp}")
            sql_expr = converter.convert(parsed_expr)
            print(f"PostgreSQL: {sql_expr}")
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            # traceback.print_exc() # Uncomment for full stack trace during debugging 