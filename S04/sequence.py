from pathlib import Path
FILENAME = "sequences/ADA.txt"
file_contents = Path(FILENAME).read_text()



def cleaner(seq):
    first_end = seq.find("\n")
    seq1 = seq[first_end:]
    seq1 = seq1.replace("\n","")
    return seq1




new_seq = cleaner(file_contents)
print(len(new_seq))
#done