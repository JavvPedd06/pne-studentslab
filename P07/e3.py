import http.client
import http.client
import json

SERVER = 'rest.ensembl.org'
GENE_NAME = 'MIR633'
GENE_ID = 'ENSG00000207562'
ENDPOINT = f'/sequence/id/{GENE_ID}'
PARAMS = '?content-type=application/json'

URL = SERVER + ENDPOINT + PARAMS
print()
print(f'SERVER {SERVER}')
print(f'URL {URL}')


conn = http.client.HTTPSConnection(SERVER)
conn.request("GET", ENDPOINT + PARAMS)
try:
    r1 = conn.getresponse()

    if r1.status == 200:
        data1 = r1.read().decode("utf-8")
        response = json.loads(data1)
        print(f"Response recieved:{r1.status} {r1.reason}")
        sequence = response.get('seq')
        description = response.get('desc')

        print(f'Gene: {GENE_NAME}')
        print(f'Description: {description}')
        print(f'Sequence: {sequence}')
    else:
        print(f"Failed to retrieve data: {r1.status} {r1.reason}")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")

conn.close()