# ==============================
# AST Generator (REAL STRUCTURE)
# Supports:
# - Variable declarations
# - Assignments
# - Expressions (+ - * /)
# - if / else
# - while loops
# - blocks { }
# D3-compatible tree format
# ==============================

class ASTBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --------------------------
    # Helpers
    # --------------------------
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return {"type": "EOF", "value": "EOF"}

    def advance(self):
        self.pos += 1

    def match(self, value):
        if self.current().get("value") == value:
            self.advance()
            return True
        return False

    # ==============================
    # ENTRY
    # ==============================
    def build(self):
        return {
            "name": "Program",
            "children": self.block(stop=[])
        }

    # ==============================
    # BLOCK PARSER
    # ==============================
    def block(self, stop):
        nodes = []

        while self.current().get("type") != "EOF" and self.current().get("value") not in stop:
            stmt = self.statement()
            if stmt:
                nodes.append(stmt)
            else:
                self.advance()

        return nodes

    # ==============================
    # STATEMENTS
    # ==============================
    def statement(self):
        token = self.current()

        if token["value"] == "if":
            return self.if_statement()

        if token["value"] == "while":
            return self.while_statement()

        if token["type"] in ["KEYWORD"]:
            return self.declaration()

        if token["type"] == "IDENTIFIER":
            return self.assignment()

        return None

    # ------------------------------
    # VARIABLE DECLARATION
    # ------------------------------
    def declaration(self):
        datatype = self.current()["value"]
        self.advance()

        name = self.current()["value"]
        self.advance()

        node = {
            "name": "Declaration",
            "children": [
                {"name": datatype},
                {"name": name}
            ]
        }

        if self.match("="):
            node["children"].append(self.expression())

        self.match(";")
        return node

    # ------------------------------
    # ASSIGNMENT
    # ------------------------------
    def assignment(self):
        name = self.current()["value"]
        self.advance()

        self.match("=")

        node = {
            "name": "Assignment",
            "children": [
                {"name": name},
                self.expression()
            ]
        }

        self.match(";")
        return node

    # ------------------------------
    # IF / ELSE
    # ------------------------------
    def if_statement(self):
        self.advance()  # if

        self.match("(")
        condition = self.expression()
        self.match(")")

        self.match("{")
        if_body = self.block(stop=["}"])
        self.match("}")

        node = {
            "name": "IfStatement",
            "children": [
                condition,
                {
                    "name": "IfBlock",
                    "children": if_body
                }
            ]
        }

        # ELSE SUPPORT
        if self.current().get("value") == "else":
            self.advance()
            self.match("{")
            else_body = self.block(stop=["}"])
            self.match("}")

            node["children"].append({
                "name": "ElseBlock",
                "children": else_body
            })

        return node

    # ------------------------------
    # WHILE LOOP
    # ------------------------------
    def while_statement(self):
        self.advance()

        self.match("(")
        condition = self.expression()
        self.match(")")

        self.match("{")
        body = self.block(stop=["}"])
        self.match("}")

        return {
            "name": "WhileLoop",
            "children": [
                condition,
                {
                    "name": "Body",
                    "children": body
                }
            ]
        }

    # ==============================
    # EXPRESSIONS (REAL TREE)
    # ==============================
    def expression(self):
        node = self.term()

        while self.current().get("value") in ["+", "-"]:
            op = self.current()["value"]
            self.advance()

            node = {
                "name": op,
                "children": [
                    node,
                    self.term()
                ]
            }

        return node

    def term(self):
        node = self.factor()

        while self.current().get("value") in ["*", "/"]:
            op = self.current()["value"]
            self.advance()

            node = {
                "name": op,
                "children": [
                    node,
                    self.factor()
                ]
            }

        return node

    def factor(self):
        token = self.current()

        if token["type"] in ["NUMBER", "IDENTIFIER"]:
            self.advance()
            return {"name": token["value"]}

        if token["value"] == "(":
            self.advance()
            node = self.expression()
            self.match(")")
            return node

        return {"name": "error"}


# ==============================
# PUBLIC API
# ==============================
def generate_ast(tokens):
    builder = ASTBuilder(tokens)
    return builder.build()