from Client0 import Client
from P01.Seq1 import Seq



FRAT1 = "../sequences/FRAT1.txt"

s = Seq()


PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.85" #This is the IP from the Pc i was working 3rd row, closest to the hallway on the left side from professors' POV
PORT = 8080

def cut(string):
    fragments = []
    for i in range(5):
        start_index = i * 10
        end_index = start_index + 10
        fragment = string[start_index:end_index]
        fragments.append(fragment)

    return fragments


c = Client(IP, PORT)
print(f"Sending the FRAT1 Gene to the server...")
fragments = cut(s.seq_read_fasta(FRAT1))
print(f"Gene FRAT1: {s.seq_read_fasta(FRAT1)}")
i = 1
for ch in fragments:
    print(f"Fragment {i}: ")

    response = c.talk(ch)
    print(f"Response: {response}")
    i = i + 1 