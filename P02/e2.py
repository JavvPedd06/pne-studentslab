from Client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.85" #This is the IP from the Pc i was working 3rd row, closest to the hallway on the left side from professors' POV
PORT = 8080

c = Client(IP, PORT)
print(c)
