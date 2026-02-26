
from Seq1 import Seq
print("-----| Practice 1 Exercise 5 |------")
seq = Seq("TATAC")
seq2 = Seq()
seq3 =Seq("Invalid")

print(f"Sequence 1: {seq} (Length: {seq.length()}) ")
bases = ["A", "C", "G", "T"]
for base in bases:
    count = seq.count_base(base)
    print(f"{base}: {count}", end="   ")
print()

print(f"Sequence 1: {seq2} (Length: {seq2.length()}) ")
bases = ["A", "C", "G", "T"]
for base in bases:
    count = seq2.count_base(base)
    print(f"{base}: {count}" , end="   ")
print()

print(f"Sequence 1: {seq3} (Length: {seq3.length()}) ")
bases = ["A", "C", "G", "T"]
for base in bases:
    count = seq3.count_base(base)
    print(f"{base}: {count}", end="   ")
print()


