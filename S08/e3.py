import socket

# SERVER IP, PORT
PORT = 8081
IP = "212.128.255.86" # depends on the computer the server is running
try:
    while True:
      message = input("Enter a message: ")

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((IP, PORT))
      s.send(message.encode())

      s.close()
except KeyboardInterrupt:
    print("Keyboard interruption")