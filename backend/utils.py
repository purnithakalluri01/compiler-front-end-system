# ==============================
# Compiler Utilities
# Compiler Front-End System
# ==============================

import time


class CompilerStats:
    """
    Tracks compiler performance metrics:
    - execution time
    - token count
    - error count
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.token_count = 0
        self.error_count = 0

    # ==========================
    # Timing Controls
    # ==========================
    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def get_time_ms(self):
        if self.start_time is None or self.end_time is None:
            return 0
        return round((self.end_time - self.start_time) * 1000, 2)

    # ==========================
    # Metrics Setters
    # ==========================
    def set_tokens(self, tokens):
        self.token_count = len(tokens)

    def set_errors(self, error_list):
        if isinstance(error_list, list):
            self.error_count = len(error_list)
        else:
            self.error_count = 1

    # ==========================
    # Final Stats Output
    # ==========================
    def build(self):
        return {
            "tokens": self.token_count,
            "errors": self.error_count,
            "time": self.get_time_ms()
        }