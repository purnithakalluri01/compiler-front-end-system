⚙ Compiler Front-End System

An interactive Compiler Front-End system that simulates the complete compilation pipeline including lexical analysis, syntax parsing, semantic analysis, symbol table management, and Abstract Syntax Tree (AST) generation with error detection and visualization.

🚀 Features

- 🔤 Lexical Analysis (Token generation from source code)
- 🌳 Syntax Analysis (Parsing and grammar validation)
- 🧠 Semantic Analysis (type checking and error detection)
- 📊 Symbol Table construction and management
- 🌲 Abstract Syntax Tree (AST) generation
- 💻 Web-based interface for code input and output
- 🧾 Multi-line code support
- ⚠️ Error reporting (lexical, syntax, semantic errors)

🧪 Example Input

int a = 10;
int b = 20;
int c = a + b;

❌ Error Test Cases
1. Undeclared Variable
b = a + 5;
2. Syntax Error (Missing semicolon)
int a = 10
int b = 20;
3. Invalid Token
int a = 10 @ 5;

🛠 Tech Stack
Python (Flask Backend)
HTML
CSS
JavaScript

⚙ Compiler Phases Implemented
Lexical Analysis → Token generation
Syntax Analysis → Structure validation
Semantic Analysis → Meaning & type checking
Symbol Table → Identifier tracking
AST Generation → Tree representation

🎯 Project Objective
To understand how a real compiler works internally by processing source code step-by-step from raw text to structured representations and error detection.

👨‍💻 Author
Purnitha Kalluri

📌 Note
This project is developed for academic learning purposes to demonstrate compiler design concepts and frontend compilation phases.
