dna = "ATGCGATCGATCGATCGATCGA"


def calculate_apperances(seq, subseq):
    subseq_len = len(subseq)
    i = 0
    count = 0
    while i < len(seq):
        if seq[i : i + subseq_len] == subseq:
            count = count + 1
            i = i + 1

        else:
            i = i + 1

    return count

def dna_to_rna(seq):
    new = ""
    for ch in seq:
        if ch == "T":
            new = new +"U"
        elif ch == "A":
            new = new +"A"
        elif ch == "G":
            new = new +"G"
        elif ch == "C":
            new = new +"C"
    return new


print("The length of the string is:", len(dna))
print("The first 5 characters are:", dna[0:5])
print("The last 3 characters are:", dna[-4:-1])
subseq = "ATC"
print("The sequence", subseq, "appears a total number of times of:", calculate_apperances(dna, subseq))
print("The sequence of dna", dna, "translated into rna is:", dna_to_rna(dna))