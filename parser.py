# ==============================
# Enhanced Syntax Analyzer (Parser)
# Supports:
# - Variable declarations
# - Assignments
# - Arithmetic expressions (+ - * /)
# - if statements
# - while loops
# - function declarations (basic)
# - detailed error reporting
# ==============================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    # ------------------------------
    # Utility functions
    # ------------------------------
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return {"type": "EOF", "value": "EOF"}

    def advance(self):
        self.pos += 1

    def match(self, token_type=None, value=None):
        token = self.current()

        if token_type and token.get("type") != token_type:
            return False
        if value and token.get("value") != value:
            return False

        self.advance()
        return True

    def expect(self, token_type=None, value=None, message="Syntax error"):
        token = self.current()

        if token_type and token.get("type") != token_type:
            self.error(message + f" at '{token.get('value')}'")
            return False

        if value and token.get("value") != value:
            self.error(message + f" expected '{value}'")
            return False

        self.advance()
        return True

    def error(self, msg):
        self.errors.append(f"Line {self.pos + 1}: {msg}")

    # ------------------------------
    # Entry point
    # ------------------------------
    def parse(self):
        while self.current().get("type") != "EOF":
            if not self.statement():
                self.advance()  # recover
        return len(self.errors) == 0, self.errors

    # ------------------------------
    # Statements
    # ------------------------------
    def statement(self):
        token = self.current()

        if token["type"] in ["KEYWORD", "DATATYPE"]:
            return self.declaration()

        elif token["type"] == "IDENTIFIER":
            return self.assignment()

        elif token["value"] == "if":
            return self.if_statement()

        elif token["value"] == "while":
            return self.while_statement()

        elif token["value"] == "function":
            return self.function_declaration()

        else:
            self.error(f"Unexpected token '{token['value']}'")
            return False

    # ------------------------------
    # Variable Declaration
    # int a = 5 ;
    # ------------------------------
    def declaration(self):
        self.advance()  # datatype

        if not self.expect("IDENTIFIER", message="Expected variable name"):
            return False

        if self.current().get("value") == "=":
            self.advance()
            if not self.expression():
                return False

        if not self.expect(value=";", message="Missing ';' after declaration"):
            return False

        return True

    # ------------------------------
    # Assignment
    # a = b + c ;
    # ------------------------------
    def assignment(self):
        self.advance()  # identifier

        if not self.expect(value="=", message="Expected '=' in assignment"):
            return False

        if not self.expression():
            return False

        if not self.expect(value=";", message="Missing ';' after assignment"):
            return False

        return True

    # ------------------------------
    # if statement
    # if ( condition ) { ... }
    # ------------------------------
    def if_statement(self):
        self.advance()  # if

        if not self.expect(value="(", message="Expected '(' after if"):
            return False

        if not self.expression():
            return False

        if not self.expect(value=")", message="Expected ')' after condition"):
            return False

        if not self.expect(value="{", message="Expected '{' after if condition"):
            return False

        while self.current().get("value") != "}" and self.current().get("type") != "EOF":
            self.statement()

        if not self.expect(value="}", message="Expected '}' after if block"):
            return False

        return True

    # ------------------------------
    # while loop
    # while ( condition ) { ... }
    # ------------------------------
    def while_statement(self):
        self.advance()

        if not self.expect(value="(", message="Expected '(' after while"):
            return False

        if not self.expression():
            return False

        if not self.expect(value=")", message="Expected ')' after condition"):
            return False

        if not self.expect(value="{", message="Expected '{' after while"):
            return False

        while self.current().get("value") != "}" and self.current().get("type") != "EOF":
            self.statement()

        if not self.expect(value="}", message="Expected '}' after while block"):
            return False

        return True

    # ------------------------------
    # function declaration
    # function name() { ... }
    # ------------------------------
    def function_declaration(self):
        self.advance()

        if not self.expect("IDENTIFIER", message="Expected function name"):
            return False

        if not self.expect(value="(", message="Expected '(' after function name"):
            return False

        if not self.expect(value=")", message="Only empty params supported now"):
            return False

        if not self.expect(value="{", message="Expected '{' for function body"):
            return False

        while self.current().get("value") != "}" and self.current().get("type") != "EOF":
            self.statement()

        if not self.expect(value="}", message="Expected '}' after function body"):
            return False

        return True

    # ------------------------------
    # Expression Parser (recursive descent)
    # Handles + - * /
    # ------------------------------
    def expression(self):
        return self.term()

    def term(self):
        if not self.factor():
            return False

        while self.current().get("value") in ["+", "-"]:
            self.advance()
            if not self.factor():
                return False

        return True

    def factor(self):
        if not self.primary():
            return False

        while self.current().get("value") in ["*", "/"]:
            self.advance()
            if not self.primary():
                return False

        return True

    def primary(self):
        token = self.current()

        if token["type"] in ["NUMBER", "IDENTIFIER"]:
            self.advance()
            return True

        if token["value"] == "(":
            self.advance()
            if not self.expression():
                return False
            if not self.expect(value=")", message="Expected ')'"):
                return False
            return True

        self.error(f"Invalid expression near '{token['value']}'")
        return False


# ==============================
# External API function
# ==============================
def parse(tokens):
    parser = Parser(tokens)
    success, errors = parser.parse()

    if success:
        return True, "Syntax analysis successful"
    return False, errors