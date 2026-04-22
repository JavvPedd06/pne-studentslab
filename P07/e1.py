import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'

URL = SERVER + ENDPOINT + PARAMS
print()
print(f'SERVER {SERVER}')
print(f'URL {URL}')

conn = http.client.HTTPSConnection(SERVER)
conn.request("GET", ENDPOINT + PARAMS)
try:
    r1 = conn.getresponse()
    data1 = r1.read().decode("utf-8")
    response = json.loads(data1)
    if response.get('ping') == 1:
        print(f"Response recieved:{r1.status} {r1.reason}")
        print("Server UP")
    else:
        print("Server down")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

conn.close()

