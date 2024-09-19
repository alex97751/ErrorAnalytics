import re
import sys

def cleanScript(file_path):
    with open(file_path, 'r') as file:
        code = file.readlines()

    single_line_comment = re.compile(r'^\s*#.*$')

    cleaned_code = []
    for line in code:
        if not single_line_comment.match(line):
            # Remove inline comments
            line = re.sub(r'#.*$', '', line).rstrip()
            if line:  # Only add non-empty lines
                cleaned_code.append(line + '\n')

    with open(file_path, 'w') as file:
        file.writelines(cleaned_code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleanScript.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    cleanScript(file_path)
    
    print(f"Comments and empty lines removed from {file_path}")
