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


def print_seqs(seq_list):
    for seq in seq_list:
        length = seq.lenth()
        sequence_str = str(seq)
        print(f"Sequence {seq}: (Length: {length}) {sequence_str}")


s3 = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
print_seqs(s3)

