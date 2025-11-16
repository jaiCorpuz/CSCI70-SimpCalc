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

import glob
import re
import sys

tokens = []
pos = 0
errors = []
output_lines = []
current_file = ""

def load_tokens(scan_filename):
    # Reads tokens from scanner output files
    scanner_token = []
    with open(scan_filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line == "":
                continue
            parts = re.split(r'\t+', line, maxsplit=1)
            if len(parts) == 1:
                parts = re.split(r'\s+', line, maxsplit=1)
            tokentype = parts[0].strip()
            lexeme = parts[1].strip() if len(parts) > 1 else ""
            scanner_token.append((tokentype, lexeme))
    return scanner_token

def current_token():
    global pos, tokens
    if pos < len(tokens):
        return tokens[pos]
    else:
        return ("EndOfFile", "")

def advance():
    global pos
    if pos < len(tokens):
        pos += 1
    return current_token()

def match(expected):
    global errors, output_lines
    scanner_token = current_token()
    if scanner_token[0] == expected:
        advance()
        return True
    else:
        errors.append(f"Symbol expected (expected '{expected}', found '{scanner_token[0]}')")
        output_lines.append("Symbol expected")
        advance()
        return False
