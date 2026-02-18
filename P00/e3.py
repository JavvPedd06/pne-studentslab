from pathlib import Path
from pathlib import Path
from P00.Seq0 import seq_len

U5 = "../sequences/U5.txt"
ADA = "../sequences/ADA.txt"
FRAT1 = "../sequences/FRAT1.txt"
FXN = "../sequences/FXN.txt"

geneU5 = Path(U5).read_text()
geneADA = Path(ADA).read_text()
geneFRAT1 = Path(FRAT1).read_text()
geneFXN = Path(FXN).read_text()


print("EXERCISE 3:")
print("Gene U5 -> Length:" , seq_len(geneU5))
print("Gene ADA -> Length:" , seq_len(geneADA))
print("Gene FRAT1 -> Length:" , seq_len(geneFRAT1))
print("Gene FXN -> Length:" , seq_len(geneFXN))


