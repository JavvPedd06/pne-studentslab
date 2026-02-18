def seq_ping():
    print("OK")

def seq_read_fasta(seq):
    first_end = seq.find("\n")
    seq1 = seq[first_end:]
    seq1 = seq1.replace("\n","")
    return seq1

def seq_len(seq):
    return len(seq)


def seq_count_base(seq):
    bases = ['A', 'T', 'G', 'C']
    total_counts = [0, 0, 0, 0]

    for gene in seq:
        for i in range(len(bases)):
            base = bases[i]
            total_counts[i] += gene.upper().count(base)

    return total_counts

def seq_printer_4(counts):
    bases = ['A', 'C', 'G', 'T']
    for i in range(len(bases)):
        print(f"  {bases[i]}: {counts[i]}")

def seq_count(seq):
    base_counter = {}
    for ch in seq:
        if ch in "ACGT":
            if ch in base_counter:
                base_counter[ch] += 1
            else:
                base_counter[ch] = 1
    return base_counter