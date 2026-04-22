import http.client
import http.client
import json
from P01.Seq1 import Seq
gene_identifiers = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6-269P": "ENSG00000206621",
    "MIR633": "ENSG00000207758",
    "TTTY4C": "ENSG00000228670",
    "RBMY2YP": "ENSG00000229352",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

SERVER = 'rest.ensembl.org'
GENE_NAME = input("Enter a gene name")
GENE_ID = gene_identifiers[GENE_NAME]
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
        s = Seq(sequence)
        dictionary_counts = s.count_bases2()
        for base, info in dictionary_counts.items():
            times = info['times']
            percent = info['percentage']
            print(f"{base}: {times} ({percent}%)")

        winner_base = None
        highest_count = -1
        for base, info in dictionary_counts.items():
            current_count = info['times']
            if current_count > highest_count:
                highest_count = current_count
                winner_base = base

        print(f"Most common base is {winner_base} with {highest_count} occurrences.")


    else:
        print(f"Failed to retrieve data: {r1.status} {r1.reason}")

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")

conn.close()