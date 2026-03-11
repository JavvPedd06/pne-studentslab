from Client0 import Client

PRACTICE = 2
EXERCISE = 3

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.86" #This is the IP from the Pc i was working 3rd row, closest to the hallway on the left side from professors' POV
PORT = 8080

c = Client(IP, PORT)
print("Sending a message to the server...")
response = c.talk("GENE RNU6_269P")
print(f"Response: {response}")
