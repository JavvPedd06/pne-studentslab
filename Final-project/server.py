import http.server
import http.client
import socketserver
import termcolor
import json
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, FileSystemLoader

# Define the code parameters
IP = "127.0.0.1"
PORT = 8080
PATH = "html"
LNK = f"http://{IP}:{PORT}"
SERVER = "rest.ensembl.org"
PAGES = ["/listSpecies", "/karyotype", "/chromosomeLength","/geneLookup", "/geneSeq", "/geneInfo", "/geneCalc", "/geneList" ]
conn = http.client.HTTPSConnection(SERVER)
env = Environment(loader=FileSystemLoader(PATH))


class TestHandler(http.server.BaseHTTPRequestHandler):

    def get_ensembl_data(self, endpoint):
        headers = {"Content-Type": "application/json"}
        conn.request("GET", endpoint, headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read().decode())
        return None

    def listSpecies(self, params):
        data = self.get_ensembl_data("/info/species")
        species_list = data.get('species', []) if data else []
        limit = int(params.get('limit', 0))
        if limit > 0:
            species_list = species_list[:limit]
        return env.get_template("list.html").render(species_list=species_list)

    def karyotype(self, params):
        species = params.get('species', '')
        data = self.get_ensembl_data(f"/info/assembly/{species}")
        karyotype = data.get('karyotype', []) if data else []
        return env.get_template("karyotype.html").render(species=species, karyotype=karyotype)

    def chromosomeLenght(self, params):
        species = params.get('species', '')
        chromo = params.get('chromo', '')
        data = self.get_ensembl_data(f"/info/assembly/{species}")
        length = "Not Found"
        if data and 'top_level_region' in data:
            for region in data['top_level_region']:
                if region['name'] == chromo:
                    length = region['length']
                    break
        return env.get_template("length.html").render(species=species, chromo=chromo, length=length)

    def geneLookup(self, params):
        gene = params.get('gene', '')
        data = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")
        gene_id = "Not Found"
        if data:
            for item in data:
                if item['type'] == "gene":
                    gene_id = item['id']
                    break

        return env.get_template("geneLookup.html").render(gene=gene,gene_id=gene_id)

    def geneSeq(self, params):
        gene = params.get('gene', '')
        data = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")
        gene_id = "Not Found"
        if data:
            for item in data:
                if item['type'] == "gene":
                    gene_id = item['id']
                    break
        sequence = "Not Found"
        if gene_id:
            seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
            if seq_data and 'seq' in seq_data:
                sequence = seq_data['seq']
        return env.get_template("geneSeq.html").render(gene=gene, gene_id=gene_id, sequence=sequence)

    def geneInfo(self, params):
        gene = params.get('gene', '')
        data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=1")

        gene_id = data.get("id", "Not Found")
        gene_name = data.get("display_name", gene)

        chromosome = data.get("seq_region_name", "Unknown")
        start = data.get("start", "Unknown")
        end = data.get("end", "Unknown")

        length = None
        if start != "Unknown" and end != "Unknown":
            length = end - start

        info = {
            "gene_id": gene_id,
            "gene_name": gene_name,
            "chromosome": chromosome,
            "start": start,
            "end": end,
            "length": length
            }

        return env.get_template("geneInfo.html").render(gene=gene,info=info)

    def geneCalc(self, params):
        gene = params.get('gene', '')
        lookup = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")

        gene_id = None

        if lookup:
            for item in lookup:
                if item.get("type") == "gene":
                    gene_id = item.get("id")
                    break

        if not gene_id:
            return env.get_template("geneCalc.html").render(gene=gene,error="Gene not found")

        seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")

        if not seq_data or "seq" not in seq_data:
            return env.get_template("geneCalc.html").render(gene=gene,error="Sequence not found")

        sequence = seq_data["seq"].upper()

        total_length = len(sequence)

        a_count = sequence.count("A")
        t_count = sequence.count("T")
        c_count = sequence.count("C")
        g_count = sequence.count("G")

        a_pct = round((a_count / total_length) * 100, 2)
        t_pct = round((t_count / total_length) * 100, 2)
        c_pct = round((c_count / total_length) * 100, 2)
        g_pct = round((g_count / total_length) * 100, 2)

        return env.get_template("geneCalc.html").render(gene=gene,gene_id=gene_id,length=total_length,a=a_pct,t=t_pct,c=c_pct,g=g_pct)

    def geneList(self, params):

        chromo = params.get('chromo', '')
        start = params.get('start', '')
        end = params.get('end', '')

        genes = []

        if chromo and start and end:

            data = self.get_ensembl_data(f"/overlap/region/human/{chromo}:{start}-{end}?feature=gene")

            if data:
                for item in data:
                    gene_name = item.get("external_name")
                    gene_id = item.get("id")

                    if gene_name:
                        genes.append({
                            "name": gene_name,
                            "id": gene_id
                        })

        return env.get_template("geneList.html").render(chromo=chromo,start=start,end=end,genes=genes)

    def do_GET(self):
        print("GET received! Request line:")
        termcolor.cprint("  " + self.requestline, 'green')
        print("  Command: " + self.command)


        parsed_url = urlparse(self.path)
        dir_path = parsed_url.path
        params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        try:
            if dir_path == "/" or dir_path == "/index.html":
                contents = env.get_template("index.html").render()
                style = "text/html"
            elif dir_path == PAGES[0]:
                contents = self.listSpecies(params)
                style = "text/html"
            elif dir_path == PAGES[1]:
                contents = self.karyotype(params)
                style = "text/html"
            elif dir_path == PAGES[2]:
                contents = self.chromosomeLenght(params)
                style = "text/html"
            elif dir_path == PAGES[3]:
                contents = self.geneLookup(params)
                style = "text/html"
            elif dir_path == PAGES[4]:
                contents = self.geneSeq(params)
                style = "text/html"
            elif dir_path == PAGES[5]:
                contents = self.geneInfo(params)
                style = "text/html"
            elif dir_path == PAGES[6]:
                contents = self.geneCalc(params)
                style = "text/html"
            elif dir_path == PAGES[7]:
                contents = self.geneList(params)
                style = "text/html"

            else:
                raise FileNotFoundError

            response_code = 200
        except FileNotFoundError:

            contents = "<html><body><h1>404 Not Found</h1><a href='/'>Back</a></body></html>"
            style = "text/html"
            response_code = 404


        contents = contents.replace("[[lnk]]", LNK)

        self.send_response(response_code)
        self.send_header('Content-Type', style)

        if style == "text/html":
            encoded_content = contents.encode('utf-8')
            self.send_header('Content-Length', len(encoded_content))
            self.end_headers()
            self.wfile.write(encoded_content)


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# Server MAIN program
Handler = TestHandler
with socketserver.TCPServer((IP, PORT), Handler) as httpd:
    print(f"Serving at {LNK}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()