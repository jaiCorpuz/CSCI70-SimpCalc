##README
##To run this file, go to the command line of where the file is located and type python Gregorio_Scanner_Python.py
##ensure that you have python already installed within your machine

# I hereby attest to the truth of the following facts:

# I have not discussed the Python code in my program with anyone
# other than my instructor or the teaching assistants and my partner for the project assigned to this course.

# I have not used Python code obtained from another student, or
# any other unauthorized source, whether modified or unmodified.

# If any Python code or documentation used in my program was
# obtained from another source, it has been clearly noted with citations in the
# comments of my program.

#Wah

#This import allows files to be found by pathnames using pattern matching rules similar to the Unix shell to scan all the files in the directory
#https://docs.python.org/3/library/glob.html
import glob
#This import provides regular expression matching operations similar to those found in Perl. This is to add the number at the end of the file similar to those
#Patterned in the sample input and outputs
#https://docs.python.org/3/library/re.html
import re

class Scanner:
    def __init__(self):
        self.tokens = []

#This definition is a switch case that handles the various states of the DFA and handles them accordingly to the token
    def gettoken(self, state, inputChar, input):
        tokens = self.tokens
        match state:
            case "0":
                if inputChar in [' ', '\t', '\n']:
                    return "0", None, input
                elif (inputChar.isalpha() or inputChar == "_"):
                    input += inputChar
                    state = "3"
                    return state, None, input
                elif inputChar.isdigit():
                    input += inputChar
                    state = "4" 
                    return state, None, input
                elif inputChar == "/":
                    input += inputChar
                    state = "1"
                    return state, None, input
                elif inputChar == "(":
                    tokens.append(("LeftParen", inputChar))
                    state = "0"
                    return state, None, input            
                elif inputChar == ")":
                    tokens.append(("RightParen", inputChar))
                    state = "0"
                    return state, None, input            
                elif inputChar == ";":
                    tokens.append(("Semicolon", inputChar))
                    state = "0"
                    return state, None, input            
                elif inputChar == ",":
                    tokens.append(("Comma", inputChar))
                    state = "0"
                    return state, None, input                     
                elif inputChar == "+":
                    tokens.append(("Plus", inputChar))
                    state = "0"
                    return state, None, input
                elif inputChar == "-":
                    tokens.append(("Minus", inputChar))
                    state = "0"
                    return state, None, input
                elif inputChar == "=":
                    tokens.append(("Equal", inputChar))
                    state = "0"
                    return state, None, input
                elif inputChar == '"':
                    input += inputChar
                    state = "10" 
                    return state, None, input
                elif inputChar == ":":
                    input += inputChar
                    state = "11" 
                    return state, None, input
                elif inputChar == "*":
                    input += inputChar
                    state = "12" 
                    return state, None, input
                elif inputChar == "<":
                    input += inputChar
                    state = "13" 
                    return state, None, input
                elif inputChar == ">":
                    input += inputChar
                    state = "14" 
                    return state, None, input
                elif inputChar == "!":
                    input += inputChar
                    state = "15" 
                    return state, None, input
                else:
                    tokens.append(("LexicalError: ", "Lexical Error: Illegal character/character sequence"))
                    state = "0"
                    input = "" 
                    return state, None, input
            case "1":
                if inputChar == "/":
                    state = "2"
                    return state, None, input
                else:
                    state = "divide"
                    return state, inputChar, input
            case "2":
                if inputChar == '\n':
                    state = "0"
                    return state, None, input
                else:
                    state = "2"
                    input = ""
                    return state, None, input
            case "3":
                if (inputChar.isalpha() or inputChar.isdigit() or inputChar == "_"):
                    state = "3"
                    input += inputChar 
                    return state, None, input 
                else:
                    state = "ident"
                    return state, None, input
            case "4":
                if inputChar.isdigit():
                    input += inputChar
                    state = "4"
                    return state, None, input
                elif (inputChar == "e" or inputChar == "E"):
                    input += inputChar
                    state = "6" 
                    return state, None, input
                elif inputChar == ".":
                    input += inputChar
                    state = "5" 
                    return state, None, input
                else:
                    state = "num"
                    return state, inputChar, input
            case "5":
                if inputChar.isdigit():
                    input += inputChar
                    state = "9"
                    return state, None, input
                else:
                    tokens.append(("LexicalError: ", "Invalid number format"))
                    state = "0"
                    input = "" 
                    return state, None, input
            case "6":
                if inputChar.isdigit():
                    input += inputChar
                    state = "8"
                    return state, None, input
                elif (inputChar == "+" or inputChar == "-"):
                    input += inputChar
                    state = "7"
                    return state, None, input
                else:
                    tokens.append(("LexicalError: ", "Invalid number format"))
                    state = "0"
                    input = "" 
                    return state, None, input
            case "7":
                if inputChar.isdigit():
                    input += inputChar
                    state = "8"
                    return state, None, input
                else:
                    tokens.append(("LexicalError: ", "Invalid number format"))
                    state = "0"
                    input = "" 
                    return state, None, input
            case "8":
                if inputChar.isdigit():
                    input += inputChar
                    state = "8"
                    return state, None, input
                else:
                    state = "num"
                    return state, inputChar, input
            case "9":
                if inputChar.isdigit():
                    input += inputChar
                    state = "9"
                    return state, None, input
                elif (inputChar == "e" or inputChar == "E"):
                    input += inputChar
                    state = "6"
                    return state, None, input
                else:
                    state = "num"
                    return state, inputChar, input
            case "10":
                if inputChar == '\n':
                    tokens.append(("LexicalError: ", "Unterminated string"))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif inputChar == '"':
                    tokens.append(("String", input + '"'))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    state = "10"
                    input += inputChar
                    return state, None, input
            case "11":
                if(inputChar == "="):
                    tokens.append(("Assign", input + "="))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    state = "colon"
                    return state, inputChar, input
            case "12":
                if(inputChar == "*"):
                    tokens.append(("Raise", input + "*"))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    state = "multiply"
                    return state, inputChar, input
            case "13":
                if(inputChar == "="):
                    tokens.append(("LTEqual", input + "="))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    state = "lessthan"
                    return state, inputChar, input
            case "14":
                if(inputChar == "="):
                    tokens.append(("GTEqual", input + "="))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    state = "greaterthan"
                    return state, inputChar, input
            case "15":
                if(inputChar == "="):
                    tokens.append(("Not Equal", input + "="))
                    state = "0"
                    input = ""
                    return state, None, input
                else:
                    tokens.append(("LexicalError: ", "Lexical Error: Illegal character/character sequence"))
                    state = "0"
                    input = "" 
                    return state, None, input
            case "divide":
                tokens.append(("Divide", input))
                state = "0"
                input = "" 
                return state, inputChar, input
            case "num":
                tokens.append(("Num", input))
                state = "0"
                input = "" 
                return state, inputChar, input
            case "ident":
                if(input == "PRINT"):
                    tokens.append(("Print", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "IF"):
                    tokens.append(("If", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "ELSE"):
                    tokens.append(("Else", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "ENDIF"):
                    tokens.append(("Endif", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "SQRT"):
                    tokens.append(("Sqrt", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "AND"):
                    tokens.append(("And", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "OR"):
                    tokens.append(("Or", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                elif(input == "NOT"):
                    tokens.append(("Not", input))
                    state = "0"
                    input = "" 
                    return state, inputChar, input
                else:
                    tokens.append(("Identifier", input))
                    state = "0"
                    input = ""
                    return state, inputChar, input
            case "colon":
                tokens.append(("Colon", input))
                state = "0"
                input = "" 
                return state, inputChar, input
            case "multiply":
                tokens.append(("Multiply", input))
                state = "0"
                input = "" 
                return state, inputChar, input
            case "lessthan":
                tokens.append(("Less Than", input))
                state = "0"
                input = "" 
                return state, inputChar, input
            case "greaterthan":
                tokens.append(("Greater Than", input))
                state = "0"
                input = "" 
                return state, inputChar, input

# This gets all of the txt files in the current directory
    def scan(self, infile):
        self.tokens = []

        match = re.search(r'(\d+)\.txt$', infile)
        if match:
            num = match.group(1)
        else:
            #If no number is found, we leave it blank, jic there is an input file like that it will still be processed and outputted :DD
            num = "" 

        # This builds the output file name to satisfy the instruction
        #"If the input file is named sample input.txt, then the output file for the scanner should be sample output scan.txt"
        base_name = "sample_output_scan"
        if num:
            outfile = f"{base_name}_{num}.txt" #adds the number like the sample files!
        else:
            outfile = f"{base_name}.txt"

        with open(infile, "r") as f:
            lines = f.readlines()

        for line in lines:
            chars = list(line)
            state = "0"
            pushback = None
            input_str = ""

            #loops through the elements of the list
            for x in chars:
                #This means if there is a pushback, meaning we have to reprocess the character
                if pushback is not None:
                    n = pushback
                    pushback = None
                    state, pushback, input_str = self.gettoken(state, n, input_str)
                
                #This is where the reprocessing happens
                state, pushback, input_str = self.gettoken(state, x, input_str)

                #This is to account for the elements that get stuck in num and arent able to process themselves so that it gets pushed out
                if state in ("num", "divide", "ident", "colon", "multiply", "lessthan", "greaterthan"):
                    state, pushback, input_str = self.gettoken(state, x, input_str)

            #This is to account for the last element that might be stuck in pushback states so that it gets pushed out
            if state in ("num", "4") and input_str != "":
                self.tokens.append(("Num", input_str))
            elif state == "1":
                self.tokens.append(("Divide", input_str))
            elif pushback is not None:
                self.gettoken(state, pushback, input_str)

        # Appends the EndOfFile after the scanning
        self.tokens.append(("EndOfFile", ""))

        # Writes everything to corresponding output file
        with open(outfile, "w") as out:
            for tokentype, tokenvalue in self.tokens:
                out.write(f"{tokentype:<17}{tokenvalue}\n")

        return outfile

    def run_inputs(self):
        input_files = glob.glob("input*.txt")  
        generated_files = []
        for infile in input_files:
            out = self.scan(infile)
            generated_files.append(out)
        return generated_files