from lexer import tokenize
from parser import parse

code = "a = b + 10"

tokens = tokenize(code)

valid, message = parse(tokens)

print("Tokens:")
print(tokens)

print("\nParser Result:")
print(valid)
print(message)