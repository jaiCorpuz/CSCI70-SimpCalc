import glob
from Corpuz_Parser_Python import Parser

scan_outputs = glob.glob("sample_output_scan*.txt")

for scan_file in scan_outputs:
    parts = scan_file.replace(".txt", "").split("_")
    num = parts[-1] if parts[-1].isdigit() else ""

    if num:
        parser_out = f"sample_output_parser_{num}.txt"
    else:
        parser_out = "sample_output_parser.txt"

    with open(parser_out, "w") as out:
        p = Parser(scan_file)
        lines = p.parse()

        # Write ONLY the parser output (including validity)
        for line in lines:
            out.write(line + "\n")
