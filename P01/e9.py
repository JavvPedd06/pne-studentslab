from Seq1 import Seq
from pathlib import Path
print("-----| Practice 1 Exercise 9 |------")
U5 = "../sequences/U5.txt"
s = Seq()
s1 = s.seq_read_fasta(U5)
seq = Seq(s1)
rev = seq.reverse()
comp = seq.seq_complement()
print(f"Sequence 1: {seq} (Length: {seq.length()}) ")
print(f"Bases: {seq.count()}")
print(f"Reverse: {rev}")
print(f"Comp: {comp}")
print()