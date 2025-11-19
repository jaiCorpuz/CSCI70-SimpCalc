from Gregorio_Scanner_Python import scan
from Corpuz_Parser_Python import Parser

scan_files = scan()

# 2. For each scan file, run the parser
for scan_file in scan_files:
    # extract number (same logic as before)
    parts = scan_file.replace(".txt", "").split("_")
    num = parts[-1] if parts[-1].isdigit() else ""

    parser_out = f"sample_output_parser_{num}.txt" if num else "sample_output_parser.txt"

    with open(parser_out, "w") as out:
        parser = Parser(scan_file)
        lines = parser.parse()
        for line in lines:
            out.write(line + "\n")
