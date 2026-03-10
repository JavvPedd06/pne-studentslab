import socket


ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


PORT = 8080
IP = "212.128.255.95"


ls.bind((IP, PORT))


ls.listen()

num_connections = 0

client_list = []

print("The server is configured!")

while True:

    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()


    except KeyboardInterrupt:
        print("Server stopped by the user")


        ls.close()


        exit()


    else:
        num_connections += 1
        client_list.append(client_ip_port)

        print(f"Connection {num_connections}")
        print(f"Client IP: {client_ip_port[0]}")
        print(f"Client Port: {client_ip_port[1]}")
        print("A client has connected to the server!")
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode()


        print(f"Message received: {msg}")

        response = f" {msg} \n"
        cs.send(response.encode())


        cs.close()


        if num_connections == 5:
            print("\n--- List of Connected Clients ---")


            for i in range(len(client_list)):
                client = client_list[i]
                print(f"Client {i + 1}: IP = {client[0]}, Port = {client[1]}")

            ls.close()
            print("Server finished after 5 connections")
            exit()