from dna_count import count_bases

if __name__ == "__main__":
    with open("dna.txt", "r") as f:
        lines = f.readlines()

    total_number = 0
    bases = {"A": 0, "C": 0, "T": 0, "G": 0}

    for sequence in lines:
        sequence = sequence.strip()
        total_number += len(sequence)
        result = count_bases(sequence)
        for key in result:
            bases[key] += result[key]

    print("Total nº of bases:", total_number)

    for base, count in bases.items():
        print(f'{base}:{count}').



