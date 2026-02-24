import termcolor
class Seq:
    def __init__(self, strbases):
        for ch in strbases:
            if ch != "A" and ch != "C" and ch != "T" and ch != "G":
                self.strbases = "ERROR!"
            else:
                self.strbases = strbases
    def __str__(self):
        return self.strbases

    def lenth(self):
        return len(self.strbases)


def generate_seq(piece, n):
    lst = []
    i = 1
    while i < n + 1:
        lst.append(Seq(piece*i))
        i = i +1
    return lst

def print_seqs(seq_list, color1):
    for seq in seq_list:
        length = seq.lenth()
        sequence_str = str(seq)
        termcolor.cprint(f"Sequence {seq}: (Length: {length}) {sequence_str}", color1)

s4 = generate_seq("A", 3)
s5 = generate_seq("AC", 5)
termcolor.cprint("LIST 1:", "blue")
print_seqs(s4, "blue")
print()
termcolor.cprint("LIST 2:", "green")
print_seqs(s5, "green")