from Seq1 import Seq
from pathlib import Path
print("-----| Practice 1, Exercise 10 |------")
U5 = "../sequences/U5.txt"
ADA = "../sequences/ADA.txt"
FRAT1 = "../sequences/FRAT1.txt"
FXN = "../sequences/FXN.txt"
RNU6_269P = "../sequences/RNU6_269P.txt"

s1 = Seq()
s11 = s1.seq_read_fasta(U5)
seq1 = Seq(s11)

s2 = Seq()
s22 = s2.seq_read_fasta(ADA)
seq2 = Seq(s22)

s3 = Seq()
s33 = s3.seq_read_fasta(FRAT1)
seq3 = Seq(s33)

s4 = Seq()
s44 = s4.seq_read_fasta(FXN)
seq4 = Seq(s44)

s5 = Seq()
s55 = s5.seq_read_fasta(RNU6_269P)
seq5 = Seq(s55)



print(f"GENE 1: U5 Most frequent base: {seq1.frequency()} ")
print()
print(f"GENE 2: ADA Most frequent base: {seq2.frequency()} ")
print()
print(f"GENE 3: FRAT1 Most frequent base: {seq3.frequency()} ")
print()
print(f"GENE 4: FXN Most frequent base: {seq4.frequency()} ")
print()
print(f"GENE 5: RNU6_269P Most frequent base: {seq5.frequency()} ")
print()