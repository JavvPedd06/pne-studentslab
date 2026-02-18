from pathlib import Path

from P00.Seq0 import seq_count

U5 = "../sequences/U5.txt"
ADA = "../sequences/ADA.txt"
FRAT1 = "../sequences/FRAT1.txt"
FXN = "../sequences/FXN.txt"

geneU5 = Path(U5).read_text()
geneADA = Path(ADA).read_text()
geneFRAT1 = Path(FRAT1).read_text()
geneFXN = Path(FXN).read_text()

gene_names = ["U5", "ADA", "FRAT1", "FXN"]
gene_sequences = [geneU5, geneADA, geneFRAT1, geneFXN]
print("EX 5:")
for i in range(len(gene_names)):
    counts = seq_count(gene_sequences[i])
    print(f"Gene {gene_names[i]}: {counts}")
