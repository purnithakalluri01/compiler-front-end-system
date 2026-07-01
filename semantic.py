# ==============================
# Semantic Analyzer (FIXED + AST-AWARE)
# ==============================

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    # --------------------------
    # MAIN ENTRY
    # --------------------------
    def analyze(self, node):
        if not isinstance(node, dict):
            return

        node_type = node.get("name")
        children = node.get("children", [])

        # Program node
        if node_type == "Program":
            for child in children:
                self.analyze(child)

        # Declaration
        elif node_type == "Declaration":
            self.handle_declaration(node)

        # Assignment
        elif node_type == "Assignment":
            self.handle_assignment(node)

        # If / While
        elif node_type in ["IfStatement", "WhileLoop"]:
            self.handle_control_flow(node)

        # Expression or leaf
        else:
            self.check_expression(node)

    # --------------------------
    # DECLARATION
    # --------------------------
    def handle_declaration(self, node):
        children = node.get("children", [])

        if len(children) < 2:
            return

        datatype = children[0]["name"]
        var_name = children[1]["name"]

        # duplicate check
        if var_name in self.symbols:
            self.errors.append(f"Duplicate declaration: {var_name}")
        else:
            self.symbols[var_name] = datatype

        # check initialization expression (if exists)
        if len(children) > 2:
            self.check_expression(children[2])

    # --------------------------
    # ASSIGNMENT
    # --------------------------
    def handle_assignment(self, node):
        children = node.get("children", [])

        if len(children) < 2:
            return

        var_name = children[0]["name"]

        # undeclared variable check
        if var_name not in self.symbols:
            self.errors.append(f"Undeclared variable: {var_name}")

        # check RHS expression
        self.check_expression(children[1])

    # --------------------------
    # CONTROL FLOW
    # --------------------------
    def handle_control_flow(self, node):
        children = node.get("children", [])

        for child in children:
            self.analyze(child)

    # --------------------------
    # EXPRESSION VALIDATION
    # --------------------------
    def check_expression(self, node):
        if not isinstance(node, dict):
            return

        name = node.get("name")
        children = node.get("children", [])

        # leaf node (variable usage)
        if not children:
            if name and name.isidentifier() and not name.isdigit():
                if name not in self.symbols:
                    self.errors.append(f"Undeclared variable used: {name}")
            return

        # recursive check
        for child in children:
            self.check_expression(child)


# ==============================
# PUBLIC FUNCTION
# ==============================
def semantic_analysis(ast):
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer.errors