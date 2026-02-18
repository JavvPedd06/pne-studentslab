from pathlib import Path

EXON = "sequences/ADA_EXONS.txt"
GENE_FILE = "../sequences/ADA.txt"
MAX_CHROMOSOMAL_POSITION = 44652852


def clean_gene(seq):
    first_end = seq.find("\n")
    seq1 = seq[first_end:]
    seq1 = seq1.replace("\n","")
    return seq1


def read_exons(filename):

    content = Path(filename).read_text()
    exon_list = []
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            exon_list.append(line.upper())
    return exon_list


def find_exon_position(sequence, exon):
    pos = sequence.find(exon)
    return pos


def calculate_chromosomal_coords(file_start, length):
    file_end = file_start + length - 1
    chrom_start = MAX_CHROMOSOMAL_POSITION - file_end
    chrom_end = MAX_CHROMOSOMAL_POSITION - file_start
    return chrom_start, chrom_end


def main():

    gene = clean_gene(Path(GENE_FILE).read_text())
    exons = read_exons(EXON)  # Returns a LIST


    print(f"{'Exon':<8} | {'Long.':<6} | {'Start':<16} | {'End'}")
    print("-" * 53)

    exon_num = 1

    for exon_seq in exons:
        file_start = find_exon_position(gene, exon_seq)


        if file_start == -1:
            print(f"Warning: Exon {exon_num} not found!")
            exon_num += 1
            continue

        length = len(exon_seq)
        chrom_start, chrom_end = calculate_chromosomal_coords(file_start, length)

        print(f"{exon_num:<8} | {length:<6} | {chrom_start:<16} | {chrom_end}")
        exon_num += 1


main()

#notdone
