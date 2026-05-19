#The whole idea of a client is to connect with the server
import http.client
import json

PORT = 8080
SERVER = '127.0.0.1'
print(f"\nConnecting to server: {SERVER}:{PORT}\n")

#This connects with the server
conn = http.client.HTTPConnection(SERVER, PORT)
try:
    #THIS IS THE KEY, this is the URL that have the things that will lately be the params
    #This is: conn.request(METHOD, URL) which oh wow, is: conn.request("GET", endpoint, headers=headers) (from the server)
    conn.request("GET", "/listSpecies?limit=5&json=1")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

#This get a response
response = conn.getresponse()
print(f"Response received!: {response.status} {response.reason}\n")

#ALSO IMPORTANT this basically reads the bytes from the server
#The .decode("utf-8") turn those bytes into a normal and legible thing
data = response.read().decode("utf-8")

#This loads the json dta into a dictionary legible for python
json_data = json.loads(data)


#UNDER THIS ARE ALL THE PRINTS FOR THE DIFFERENT THINGS THE SERVER CAN DO
print("SPECIES LIST:\n")
for species in json_data["species"]:
    print(species["display_name"])
try:
    conn.request("GET", "/karyotype?species=homo_sapiens&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nKARYOTYPE:\n")
print("Species:", json_data["species"])
for chromosome in json_data["karyotype"]:
    print(chromosome)
try:
    conn.request("GET", "/chromosomeLength?species=homo_sapiens&chromo=1&json=1")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nCHROMOSOME LENGTH:\n")
print("Species:", json_data["species"])
print("Chromosome:", json_data["chromosome"])
print("Length:", json_data["length"])
try:
    conn.request("GET", "/geneLookup?gene=BRCA2&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nGENE LOOKUP:\n")
print("Gene:", json_data["gene"])
print("Gene ID:", json_data["gene_id"])
try:
    conn.request("GET", "/geneSeq?gene=BRCA2&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nGENE SEQUENCE:\n")
print("Gene:", json_data["gene"])
print("Gene ID:", json_data["gene_id"])
print("Sequence:")
print(json_data["sequence"])
try:
    conn.request("GET", "/geneInfo?gene=BRCA2&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nGENE INFO:\n")
print("Gene:", json_data["gene"])
info = json_data["info"]
print("Gene ID:", info["gene_id"])
print("Gene Name:", info["gene_name"])
print("Chromosome:", info["chromosome"])
print("Start:", info["start"])
print("End:", info["end"])
print("Length:", info["length"])
try:
    conn.request("GET", "/geneCalc?gene=BRCA2&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nGENE CALCULATIONS:\n")
print("Gene:", json_data["gene"])
print("Gene ID:", json_data["gene_id"])
print("Sequence Length:", json_data["length"])
print("\nBase Percentages:")
print("A:", json_data["A"], "%")
print("C:", json_data["C"], "%")
print("G:", json_data["G"], "%")
print("T:", json_data["T"], "%")

try:
    conn.request("GET", "/geneList?chromo=1&start=1000000&end=2000000&json=1")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
response = conn.getresponse()
data = response.read().decode("utf-8")
json_data = json.loads(data)


print("\nGENE LIST:\n")
print("Chromosome:", json_data["chromosome"])
print("Start:", json_data["start"])
print("End:", json_data["end"])
print("\nGenes:\n")
for gene in json_data["genes"]:
    print("Name:", gene["name"])
    print("ID:", gene["id"])
    print()

conn.close()