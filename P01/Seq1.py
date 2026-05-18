from pathlib import Path
from pathlib import Path


class Seq:

    def __init__(self, strbases=None):

        if strbases is None:

            self.strbases = "NULL"

        else:

            valid = True

            for ch in strbases:

                if ch not in "ACTG":
                    valid = False
                    break

            if valid:
                self.strbases = strbases
            else:
                self.strbases = "ERROR!"

        if self.strbases == "NULL":
            print("NULL sequence created")

        elif self.strbases == "ERROR!":
            print("INVALID sequence!")

        else:
            print("New sequence created!")

    def __str__(self):

        return self.strbases

    def length(self):

        if self.strbases in ["NULL", "ERROR!"]:
            return 0

        return len(self.strbases)

    def count_base(self, base):

        if self.strbases in ["NULL", "ERROR!"]:
            return 0

        return self.strbases.count(base)

    def count_bases2(self):

        bases = {
            "A": 0,
            "C": 0,
            "T": 0,
            "G": 0
        }

        for base in self.strbases:

            if base in bases:
                bases[base] += 1

        total = len(self.strbases)

        result = {}

        for base in ["A", "C", "G", "T"]:

            percentage = 0.0

            if total > 0:
                percentage = round(
                    (bases[base] / total) * 100,
                    1
                )

            result[base] = {
                "times": bases[base],
                "percentage": percentage
            }

        return result

    def reverse(self):

        if self.strbases in ["NULL", "ERROR!"]:
            return self.strbases

        return self.strbases[::-1]

    def seq_complement(self):

        if self.strbases in ["NULL", "ERROR!"]:
            return self.strbases

        complementary_sequence = ""

        for base in self.strbases:

            if base == "A":
                complementary_sequence += "T"

            elif base == "T":
                complementary_sequence += "A"

            elif base == "C":
                complementary_sequence += "G"

            elif base == "G":
                complementary_sequence += "C"

        return complementary_sequence

    def seq_read_fasta(self, filepath):

        self.strbases = Path(filepath).read_text()

        first_end = self.strbases.find("\n")

        seq1 = self.strbases[first_end:]

        seq1 = seq1.replace("\n", "")

        return seq1

    def frequency(self):

        if self.strbases in ["NULL", "ERROR!"]:
            return "Not valid sequence"

        bases = {
            "A": 0,
            "C": 0,
            "T": 0,
            "G": 0
        }

        for base in self.strbases:

            if base in bases:
                bases[base] += 1

        max_base = None
        max_freq = 0

        for base in bases:

            if bases[base] > max_freq:

                max_freq = bases[base]
                max_base = base

        return max_base