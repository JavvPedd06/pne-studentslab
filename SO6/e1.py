class Seq:
    def __init__(self, strbases):
        for ch in strbases:
            if ch != "A" and ch != "C" and ch != "T" and ch != "G":
                self.strbases = "ERROR!"
            else:
                self.strbases = strbases
    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)


s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")

