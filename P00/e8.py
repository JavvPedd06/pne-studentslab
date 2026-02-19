from P00.Seq0 import base_count, frequency
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

print("EX 8:")
for i in range(len(gene_names)):
    most_repeated= frequency((base_count(gene_sequences[i])))
    print(f"Gene {gene_names[i]}: Most frequent Base: {most_repeated}")
