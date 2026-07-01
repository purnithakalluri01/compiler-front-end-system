# ==============================
# Lexer (Token Generator)
# Compiler Front-End System
# ==============================

import re

KEYWORDS = {"int", "float", "char", "double", "return", "if", "else", "while", "function"}

OPERATORS = {"+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">="}

SYMBOLS = {";", "(", ")", "{", "}", ","}


def tokenize(code):
    """
    Converts source code into tokens
    """

    pattern = r"[A-Za-z_][A-Za-z0-9_]*|\d+|==|!=|<=|>=|[+\-*/=;(){}.,<>]"

    raw_tokens = re.findall(pattern, code)

    tokens = []

    for token in raw_tokens:

        if token in KEYWORDS:
            ttype = "KEYWORD"

        elif token in OPERATORS:
            ttype = "OPERATOR"

        elif token in SYMBOLS:
            ttype = "SYMBOL"

        elif token.isdigit():
            ttype = "NUMBER"

        else:
            ttype = "IDENTIFIER"

        tokens.append({
            "type": ttype,
            "value": token
        })

    return tokens