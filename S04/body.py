from pathlib import Path
FILENAME = "sequences/U5.txt"
file_contents = Path(FILENAME).read_text()

def cleaner(seq):
    first_end = seq.find("\n")
    seq1 = seq[first_end:]
    return seq1

print(cleaner(file_contents))