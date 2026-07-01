from backend.parser import parse
from backend.ast_generator import generate_ast
from backend.semantic import semantic_analysis

# --------------------------
# Sample TOKENS (manual test)
# --------------------------
tokens = [
    {"type": "DATATYPE", "value": "int"},
    {"type": "IDENTIFIER", "value": "a"},
    {"type": "OPERATOR", "value": "="},
    {"type": "NUMBER", "value": "5"},
    {"type": "SYMBOL", "value": ";"},

    {"type": "IDENTIFIER", "value": "a"},
    {"type": "OPERATOR", "value": "="},
    {"type": "IDENTIFIER", "value": "b"},
    {"type": "OPERATOR", "value": "+"},
    {"type": "IDENTIFIER", "value": "c"},
    {"type": "SYMBOL", "value": ";"}
]

# --------------------------
# Step 1: Parser
# --------------------------
success, result = parse(tokens)
print("PARSER:")
print(success, result)

# --------------------------
# Step 2: AST
# --------------------------
ast = generate_ast(tokens)
print("\nAST:")
print(ast)

# --------------------------
# Step 3: Semantic
# --------------------------
errors = semantic_analysis(ast)
print("\nSEMANTIC ERRORS:")
print(errors)