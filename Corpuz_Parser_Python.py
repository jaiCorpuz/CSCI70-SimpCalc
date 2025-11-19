##README
##To run this file, go to the command line of where the file is located and type python Corpuz_Parser_Python.py
##ensure that you have python already installed within your machine

# I hereby attest to the truth of the following facts:

# I have not discussed the Python code in my program with anyone
# other than my instructor or the teaching assistants and my partner for the project assigned to this course.

# I have not used Python code obtained from another student, or
# any other unauthorized source, whether modified or unmodified.

# If any Python code or documentation used in my program was
# obtained from another source, it has been clearly noted with citations in the
# comments of my program.

#This import allows files to be found by pathnames using pattern matching rules similar to the Unix shell to scan all the files in the directory
#https://docs.python.org/3/library/glob.html 
import re

class Parser:
    # Initializes the parser using the scanner output file
    def __init__(self, token_file):
        self.inputname = token_file
        # Extracts the tokens and lexemes
        self.tokens, self.lexemes = self.load_tokens(token_file)
        # Ensures the last token is EOF
        if not self.tokens or self.tokens[-1] != "EndOfFile":
            self.tokens.append("EndOfFile")
            self.lexemes.append("")
        # Starts reading tokens from index 0
        self.index = 0
        self.current_token = self.tokens[self.index] if self.tokens else "EndOfFile"
        self.output_lines = []
        self.errors = []

    # Load tokens from scanner output and converts it into token and lexeme lists
    def load_tokens(self, filename):
        tokens = []
        lexemes = []
        with open(filename, "r") as f:
            for line in f:
                s = line.rstrip("\n")
                if not s.strip():
                    continue
                
                # Splits on 2 or more spaces
                # Accounts for Multi-word Tokens
                parts = re.split(r'\s{2,}', s)
                if len(parts) == 1:
                    parts = re.split(r'\s+', s, maxsplit=1)

                # Takes the token type and lexeme
                tok = parts[0].strip()
                lex = parts[1].strip() if len(parts) > 1 else ""

                # Appends to list
                tokens.append(tok)
                lexemes.append(lex)
        return tokens, lexemes

    # Utilities
    # --------------------------------------------------
    # Move the parser forward to the next token
    # Ensures parser never crashes due to going beyond EOF
    def advance(self):
        # Move forward safely
        if self.index < len(self.tokens) - 1:
            self.index += 1
            self.current_token = self.tokens[self.index]
        else:
            # Already at or beyond last token -> set EOF
            self.index = len(self.tokens) - 1
            self.current_token = "EndOfFile"

    def expect(self, token_type):
        if self.current_token == token_type:
            self.advance()
        else:
            self.errors.append(f"Expected {token_type}, got {self.current_token}")
            raise Exception(f"Syntax Error: Expected {token_type}, got {self.current_token}")


    # Main parse entry
    # --------------------------------------------------
    def parse(self):
        try:
            self.program()
        except Exception:
            # parsing errors are recorded in self.errors; we continue to finalize output
            pass

        # Determine original input filename (reconstruct input#.txt)
        m = re.search(r'sample_output_scan_(\d+)\.txt$', self.inputname)
        if m:
            num = m.group(1)
            original = f"input{num}.txt"
        else:
            original = self.inputname.replace("sample_output_scan", "input")

        if not self.errors:
            self.output_lines.append(f"{original} is a valid SimpCalc program")
        else:
            self.output_lines.append(f"{original} is not a valid SimpCalc program")

        return self.output_lines
        

    # Grammar rules
    # --------------------------------------------------
    def program(self):
        while self.current_token != "EndOfFile":
            if self.current_token in ("Identifier", "Print", "If"):
                self.stmt()
            else:
                self.errors.append(f"Unexpected token {self.current_token}")
                break
        self.expect("EndOfFile")

    # stmt_list → continues until Else, Endif, or EndOfFile
    def stmt_list(self):
        # Top-level statements stop only at EOF
        while self.current_token not in ("EndOfFile",):
            if self.current_token in ("Identifier", "Print", "If"):
                self.stmt()
            else:
                # If an Else/Endif appears at top level, it belongs to a block
                if self.current_token in ("Else", "Endif"):
                    return
                self.errors.append(f"Unexpected token {self.current_token}")
                return

    def stmt_list_block(self):
        while self.current_token not in ("Else", "Endif"):
            if self.current_token == "Semicolon":
                self.advance()
            if self.current_token in ("Identifier", "Print", "If"):
                self.stmt()
            else:
                self.errors.append(f"Unexpected token in block: {self.current_token}")
                break

    def stmt(self):
        if self.current_token == "Identifier":
            self.assign_stmt()
        elif self.current_token == "Print":
            self.print_stmt()
        elif self.current_token == "If":
            self.if_stmt()
        else:
            self.errors.append(f"Unexpected token {self.current_token}")
            raise Exception(f"Syntax Error: Unexpected token {self.current_token}")

    # assignment → Identifier Assign expr [Semicolon]
    def assign_stmt(self):
        self.expect("Identifier")
        self.expect("Assign")
        self.expr()
        # allow optional semicolon before block boundary (but require it normally)
        if self.current_token == "Semicolon":
            self.expect("Semicolon")
        self.output_lines.append("Assignment Statement Recognized")

    # print → Print LeftParen expr_list RightParen [Semicolon]
    def print_stmt(self):
        self.expect("Print")
        self.expect("LeftParen")
        self.expr_list()
        self.expect("RightParen")
        if self.current_token == "Semicolon":
            self.expect("Semicolon")
        self.output_lines.append("Print Statement Recognized")

    # if → If expr Colon stmt_list Else stmt_list Endif [Semicolon]
    def if_stmt(self):
        self.expect("If")
        self.expr()
        self.expect("Colon")

        self.output_lines.append("If Statement Begins")

        self.stmt_list_block()

        # OPTIONAL ELSE
        if self.current_token == "Else":
            self.expect("Else")
            self.stmt_list_block()

        self.expect("Endif")

        if self.current_token == "Semicolon":
            self.expect("Semicolon")

        self.output_lines.append("If Statement Ends")

    # expression list: expr (Comma expr)*
    def expr_list(self):
        self.expr()
        while self.current_token == "Comma":
            self.expect("Comma")
            self.expr()

    # expr → handles basic literal/identifier, unary minus, parentheses
        # expr → primary (operator primary)*
    def expr(self):
        self.primary()

        # operators allowed in SimpCalc
        operator_tokens = {
            "Plus", "Minus", "Multiply", "Divide",
            "Raise",

            # relational operators your scanner outputs
            "Greater Than",   # >
            "Less Than",      # <
            "GTEqual",        # >=
            "LTEqual",        # <=
            "Not Equal",      # !=
            "Equal",          # =

            # Logical
            "And", "Or"
        }

        while self.current_token in operator_tokens:
            self.advance()      # consume operator
            self.primary()      # consume next part of expression

    def primary(self):
        if self.current_token in ("Identifier", "Num", "String"):
            self.advance()

        elif self.current_token in ("Minus", "Not"):      # unary negation
            self.advance()
            self.primary()

        elif self.current_token == "LeftParen":
            self.advance()
            self.expr()
            self.expect("RightParen")

        elif self.current_token == "Sqrt":       # function call: SQRT(expr)
            self.advance()
            self.expect("LeftParen")
            self.expr()
            self.expect("RightParen")

        else:
            self.errors.append(f"Unexpected token in expression: {self.current_token}")
            raise Exception(f"Syntax Error in expression: {self.current_token}")



