from Gregorio_Scanner_Python import Scanner
from Corpuz_Parser_Python import Parser

# 1. Run Scanner -> returns list of scan output files
scanner = Scanner()
scan_outputs = scanner.run_inputs()

# 2. For each scan output, run parser
for scan_file in scan_outputs:
    num = scan_file.replace(".txt", "").split("_")[-1]
    parser_out = f"sample_output_parser_{num}.txt"

    p = Parser(scan_file)
    lines = p.parse()

    with open(parser_out, "w") as f:
        for line in lines:
            f.write(line + "\n")

