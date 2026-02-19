from P00.Seq0 import seq_complement
from P00.Seq0 import seq_read_fasta
from pathlib import Path


U5 = "../sequences/U5.txt"
ADA = "../sequences/ADA.txt"
FRAT1 = "../sequences/FRAT1.txt"
FXN = "../sequences/FXN.txt"

geneU5 = Path(U5).read_text()
geneADA = Path(ADA).read_text()
geneFRAT1 = Path(FRAT1).read_text()
geneFXN = Path(FXN).read_text()

cleanU5 = seq_read_fasta(geneU5)
cleanADA = seq_read_fasta(geneADA)
cleanFRAT1 = seq_read_fasta(geneFRAT1)
cleanFXN= seq_read_fasta(geneFXN)

gene_names = ["U5", "ADA", "FRAT1", "FXN"]
gene_sequences = [cleanU5, cleanADA, cleanFRAT1, cleanFXN]

print("EX 7:")
for i in range(len(gene_names)):
    counts = seq_complement(gene_sequences[i], 20)
    print(f"Gene {gene_names[i]}:")
    print(f"Frag: {gene_sequences[i][0:20]}")
    print(f"Comp: {counts}")
    print()