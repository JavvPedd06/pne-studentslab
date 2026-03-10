from Client0 import Client

PRACTICE = 2
EXERCISE = 3

i = 0
while i < 5:
    IP = "212.128.255.95" #This is the IP from the Pc i was working 3rd row, closest to the hallway on the left side from professors' POV
    PORT = 8080

    c = Client(IP, PORT)

    print("Sending a message to the server...")

    response = c.talk(f"Message: {i}")

    print(f"Response: {response}")
    i = i + 1
