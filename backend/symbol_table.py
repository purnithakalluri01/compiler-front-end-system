# ==============================
# Symbol Table Generator
# Compiler Front-End System
# ==============================

class SymbolTable:
    def __init__(self):
        self.table = {}

    # --------------------------
    # Add Variable
    # --------------------------
    def declare(self, name, datatype, value="", scope="Global"):

        if name not in self.table:
            self.table[name] = {
                "identifier": name,
                "type": datatype,
                "value": value,
                "scope": scope
            }

    # --------------------------
    # Update Variable Value
    # --------------------------
    def assign(self, name, value):

        if name in self.table:
            self.table[name]["value"] = value

    # --------------------------
    # Check Declaration
    # --------------------------
    def exists(self, name):
        return name in self.table

    # --------------------------
    # Get Variable
    # --------------------------
    def get(self, name):
        return self.table.get(name)

    # --------------------------
    # Export
    # --------------------------
    def export(self):
        return list(self.table.values())


# =====================================
# Generate Symbol Table From Tokens
# =====================================

def generate_symbol_table(tokens):

    symbol_table = SymbolTable()

    i = 0

    while i < len(tokens):

        token = tokens[i]

        if (
            token.get("type") == "KEYWORD"
            and token.get("value") in ["int", "float", "char", "double"]
        ):

            if i + 1 < len(tokens):

                identifier = tokens[i + 1]["value"]

                value = ""

                if (
                    i + 3 < len(tokens)
                    and tokens[i + 2]["value"] == "="
                ):
                    value = tokens[i + 3]["value"]

                symbol_table.declare(
                    identifier,
                    token["value"],
                    value,
                    "Global"
                )

        i += 1

    return symbol_table.export()