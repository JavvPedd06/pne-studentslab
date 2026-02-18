from pathlib import Path
FILENAME = "../sequences/RNU6_269P.txt"
file_contents = Path(FILENAME).read_text()

def extract_header(text):
    for line in text.splitlines():
        if line.startswith('>'):
            print(line)

extract_header(file_contents)#done


