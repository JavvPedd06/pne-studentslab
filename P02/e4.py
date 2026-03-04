
from Client0 import Client
from P01.Seq1 import Seq



U5 = "../sequences/U5.txt"
ADA = "../sequences/ADA.txt"
FRAT1 = "../sequences/FRAT1.txt"

s = Seq()

gene = {"U5": U5, "ADA": ADA, "FRAT1": FRAT1}


PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.85" #This is the IP from the Pc i was working 3rd row, closest to the hallway on the left side from professors' POV
PORT = 8080

c = Client(IP, PORT)
for gene_name, gene_fasta in gene.items():
    print(f"Sending the {gene_name} Gene to the server...")
    response = c.talk(s.seq_read_fasta(gene_fasta))
    print(f"Response: {response}")