from lexer import tokenize
from parser import parse
from ast_generator import generate_ast

code = "a = b + 10"

tokens = tokenize(code)

valid, message = parse(tokens)

if valid:
    ast = generate_ast(tokens)

    print("TOKENS")
    print(tokens)

    print("\nAST")
    print(ast)

else:
    print(message)