
sequence = input("Introduce the sequence: ").upper()


count_A = 0
count_C = 0
count_T = 0
count_G = 0


for base in sequence:
    if base == 'A':
        count_A += 1
    elif base == 'C':
        count_C += 1
    elif base == 'T':
        count_T += 1
    elif base == 'G':
        count_G += 1



total_length = len(sequence)


print(f"Total length: {total_length}")
print(f"A: {count_A}")
print(f"C: {count_C}")
print(f"T: {count_T}")
print(f"G: {count_G}")