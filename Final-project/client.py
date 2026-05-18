import socket
import json


class Client:

    def __init__(self, IP, PORT):

        self.ip = IP
        self.port = PORT

    def ping(self):

        print("OK")

    def __str__(self):

        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    # --------------------------------
    # LOW LEVEL HTTP REQUEST
    # --------------------------------

    def talk(self, path):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((self.ip, self.port))

        request = f"GET {path} HTTP/1.1\r\n"
        request += f"Host: {self.ip}:{self.port}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"

        s.send(request.encode())

        response = b""

        while True:

            chunk = s.recv(4096)

            if not chunk:
                break

            response += chunk

        s.close()

        return response.decode()

    def get_json(self, path):

        response = self.talk(path)

        headers, body = response.split("\r\n\r\n", 1)

        body = body.strip()

        return json.loads(body)



client = Client("127.0.0.1", 8080)

print(client)

# --------------------------------
# TEST 1: GENE LOOKUP
# --------------------------------

data = client.get_json(
    "/geneLookup?gene=BRCA2&json=1"
)

print("\nGENE LOOKUP")
print("------------")

print("Gene:", data["gene"])
print("Gene ID:", data["gene_id"])


# --------------------------------
# TEST 2: GENE CALC
# --------------------------------

data = client.get_json(
    "/geneCalc?gene=FRAT1&json=1"
)

print("\nGENE CALC")
print("----------")

print("Gene:", data["gene"])
print("Gene ID:", data["gene_id"])
print("Length:", data["length"])
print("A%:", data["A"])
print("C%:", data["C"])
print("G%:", data["G"])
print("T%:", data["T"])


# --------------------------------
# TEST 3: SPECIES LIST
# --------------------------------

data = client.get_json(
    "/listSpecies?limit=3&json=1"
)

print("\nSPECIES")
print("--------")

for sp in data["species"]:
    print(sp["display_name"])