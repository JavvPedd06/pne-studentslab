from cola.hotkeys import RETURN


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


def seq_reverse(seq, n):
    seq2 = seq[0:n]
    return seq2[::-1]

def seq_complement(sequence, n):
    sequence2 = sequence[0:n]
    complementary_sequence = ""

    for base in sequence2:
        if base == 'A':
            complementary_sequence = complementary_sequence + "T"
        elif base == 'T':
            complementary_sequence = complementary_sequence + "A"
        elif base == 'C':
            complementary_sequence = complementary_sequence + "G"
        elif base == 'G':
            complementary_sequence = complementary_sequence + "C"
        else:
            complementary_sequence = complementary_sequence + base

    return complementary_sequence

def base_count(seq):
    base_counts = {}
    for base in seq:
        if base in base_counts:
            base_counts[base] = base_counts[base] + 1
        else:
            base_counts[base] = 1

    return base_counts

def frequency(dicc):
    valor_max = None
    freq_max = 0
    for valor in dicc:
        if dicc[valor] > freq_max:
            freq_max = dicc[valor]
            valor_max = valor

    return valor_max



