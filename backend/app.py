from flask import Flask, render_template, request, jsonify

from backend.lexer import tokenize
from backend.parser import parse
from backend.ast_generator import generate_ast
from backend.semantic import semantic_analysis
from backend.symbol_table import generate_symbol_table

import os

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# ==============================
# MAIN COMPILER PIPELINE
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compile", methods=["POST"])
def compile_code():

    data = request.get_json()
    code = data.get("code", "")

    console = []
    errors = []

    # --------------------------
    # 1. LEXER
    # --------------------------
    tokens = tokenize(code)
    console.append("✔ Lexical Analysis Completed")

    # --------------------------
    # 2. PARSER
    # --------------------------
    parse_result, parse_msg = parse(tokens)

    if parse_result:
        console.append("✔ Syntax Analysis Completed")
    else:
        console.append("❌ Syntax Analysis Failed")
        errors.append(parse_msg)

    # --------------------------
    # 3. AST GENERATION
    # --------------------------
    ast = generate_ast(tokens)
    console.append("✔ AST Generated Successfully")

    # --------------------------
    # 4. SYMBOL TABLE
    # --------------------------
    symbol_table = generate_symbol_table(tokens)
    console.append("✔ Symbol Table Generated")

    # --------------------------
    # 5. SEMANTIC ANALYSIS
    # --------------------------
    semantic_errors = semantic_analysis(ast)

    if semantic_errors:
        errors.extend(semantic_errors)
        console.append("❌ Semantic Analysis Failed")
    else:
        console.append("✔ Semantic Analysis Completed")

    # --------------------------
    # 6. STATISTICS
    # --------------------------
    stats = {
        "tokens": len(tokens),
        "identifiers": sum(1 for t in tokens if t["type"] == "IDENTIFIER"),
        "operators": sum(1 for t in tokens if t["type"] == "OPERATOR"),
        "keywords": sum(1 for t in tokens if t["type"] == "KEYWORD"),
        "numbers": sum(1 for t in tokens if t["type"] == "NUMBER"),
        "errors": len(errors)
    }

    # --------------------------
    # 7. PHASE STATUS
    # --------------------------
    phases = {
        "Lexical Analysis": "Completed",
        "Syntax Analysis": "Completed" if not errors else "Failed",
        "Semantic Analysis": "Completed" if not semantic_errors else "Failed",
        "Symbol Table": "Completed",
        "AST Generation": "Completed"
    }

    # --------------------------
    # RESPONSE
    # --------------------------
    return jsonify({
        "tokens": tokens,
        "statistics": stats,
        "symbol_table": symbol_table,
        "ast": ast,
        "console": console,
        "errors": errors,
        "phases": phases,
        "status": "SUCCESS" if not errors else "FAILED"
    })


# ==============================
# RUN SERVER (DEPLOYMENT READY)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)