from pathlib import Path
from P00.Seq0 import seq_read_fasta

FILENAME = "../sequences/U5.txt"

gene = Path(FILENAME).read_text()

clean = seq_read_fasta(gene)
final = clean[0:20]

print("DNA File: U5.txt")
print("The first 20 bases are:")
print(final)

