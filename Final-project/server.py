import http.server
import http.client
import socketserver
import termcolor
import json
import sys
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, FileSystemLoader
sys.path.append("../P01")
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080
PATH = "html"
LNK = f"http://{IP}:{PORT}"
SERVER = "rest.ensembl.org"
PAGES = [
    "/listSpecies",
    "/karyotype",
    "/chromosomeLength",
    "/geneLookup",
    "/geneSeq",
    "/geneInfo",
    "/geneCalc",
    "/geneList"
]

env = Environment(loader=FileSystemLoader(PATH))
class TestHandler(http.server.BaseHTTPRequestHandler):
    def get_ensembl_data(self, endpoint):
        conn = http.client.HTTPSConnection(SERVER)
        headers = {"Content-Type": "application/json"}
        conn.request("GET", endpoint, headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read().decode())
        return None



    def wants_json(self, params):
        return params.get("json") == "1"



    def listSpecies(self, params):
        data = self.get_ensembl_data("/info/species")
        species_list = data.get("species", []) if data else []
        limit = int(params.get("limit", 0))
        if limit > 0:
            species_list = species_list[:limit]
        result = {"species": species_list}
        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("list.html").render(species_list=species_list)
        return html, "text/html"



    def karyotype(self, params):
        species = params.get("species", "")
        data = self.get_ensembl_data(f"/info/assembly/{species}")
        karyotype = data.get("karyotype", []) if data else []
        result = {
            "species": species,
            "karyotype": karyotype}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("karyotype.html").render(
            species=species,
            karyotype=karyotype)

        return html, "text/html"



    def chromosomeLength(self, params):
        species = params.get("species", "")
        chromo = params.get("chromo", "")

        data = self.get_ensembl_data(f"/info/assembly/{species}")
        length = "Not Found"

        if data and "top_level_region" in data:
            for region in data["top_level_region"]:
                if region["name"] == chromo:
                    length = region["length"]
                    break

        result = {
            "species": species,
            "chromosome": chromo,
            "length": length}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("length.html").render(species=species,chromo=chromo,length=length)
        return html, "text/html"



    def geneLookup(self, params):
        gene = params.get("gene", "")
        data = self.get_ensembl_data(
            f"/xrefs/symbol/homo_sapiens/{gene}")

        gene_id = "Not Found"
        if data:
            for item in data:
                if item["type"] == "gene":
                    gene_id = item["id"]
                    break

        result = {
            "gene": gene,
            "gene_id": gene_id}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneLookup.html").render(gene=gene,gene_id=gene_id)
        return html, "text/html"



    def geneSeq(self, params):
        gene = params.get("gene", "")
        data = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")
        gene_id = "Not Found"

        if data:
            for item in data:
                if item["type"] == "gene":
                    gene_id = item["id"]
                    break
        sequence = "Not Found"

        if gene_id != "Not Found":
            seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")
            if seq_data and "seq" in seq_data:
                sequence = seq_data["seq"]

        result = {
            "gene": gene,
            "gene_id": gene_id,
            "sequence": sequence}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneSeq.html").render(gene=gene,gene_id=gene_id,sequence=sequence)

        return html, "text/html"


    def geneInfo(self, params):
        gene = params.get("gene", "")
        data = self.get_ensembl_data(
            f"/lookup/symbol/homo_sapiens/{gene}?expand=1")

        if not data:
            data = {}

        gene_id = data.get("id", "Not Found")
        gene_name = data.get("display_name", gene)
        chromosome = data.get("seq_region_name","Unknown")

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

        result = {"gene": gene,"info": info}

        if self.wants_json(params):
            return json.dumps(result), "application/json"
        html = env.get_template("geneInfo.html").render(gene=gene,info=info)

        return html, "text/html"

    def geneCalc(self, params):
        gene = params.get("gene", "")
        lookup = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")

        gene_id = None
        if lookup:
            for item in lookup:
                if item.get("type") == "gene":
                    gene_id = item.get("id")
                    break

        if not gene_id:
            result = {"gene": gene,"error": "Gene not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html").render(gene=gene,error="Gene not found")
            return html, "text/html"

        seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")

        if not seq_data or "seq" not in seq_data:
            result = {"gene": gene,"error": "Sequence not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html").render(gene=gene,error="Sequence not found")

            return html, "text/html"



        sequence = seq_data["seq"].upper()
        seq = Seq(sequence)
        length = seq.length()
        bases = seq.count_bases2()

        a_pct = bases["A"]["percentage"]
        c_pct = bases["C"]["percentage"]
        g_pct = bases["G"]["percentage"]
        t_pct = bases["T"]["percentage"]

        result = {
            "gene": gene,
            "gene_id": gene_id,
            "length": length,
            "A": a_pct,
            "C": c_pct,
            "G": g_pct,
            "T": t_pct
        }

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneCalc.html").render(gene=gene,gene_id=gene_id,length=length,a=a_pct,c=c_pct,g=g_pct,t=t_pct)

        return html, "text/html"


    def geneList(self, params):
        chromo = params.get("chromo", "")
        start = params.get("start", "")
        end = params.get("end", "")
        genes = []
        if chromo and start and end:
            data = self.get_ensembl_data(
                f"/overlap/region/human/{chromo}:{start}-{end}?feature=gene")

            if data:
                for item in data:
                    gene_name = item.get("external_name")

                    gene_id = item.get("id")
                    if gene_name:
                        genes.append({"name": gene_name,"id": gene_id})

        result = {
            "chromosome": chromo,
            "start": start,
            "end": end,
            "genes": genes}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneList.html").render(chromo=chromo,start=start,end=end,genes=genes)
        return html, "text/html"

    def do_GET(self):
        print("GET received!")
        termcolor.cprint("  " + self.requestline,"green")
        parsed_url = urlparse(self.path)
        dir_path = parsed_url.path
        params = {k: v[0]for k, v in parse_qs(parsed_url.query).items()}

        try:

            if dir_path == "/" or dir_path == "/index.html":
                contents = env.get_template("index.html").render()
                style = "text/html"

            elif dir_path == PAGES[0]:

                contents, style = self.listSpecies(params)

            elif dir_path == PAGES[1]:

                contents, style = self.karyotype(params)

            elif dir_path == PAGES[2]:

                contents, style = self.chromosomeLength(params)

            elif dir_path == PAGES[3]:

                contents, style = self.geneLookup(params)

            elif dir_path == PAGES[4]:

                contents, style = self.geneSeq(params)

            elif dir_path == PAGES[5]:

                contents, style = self.geneInfo(params)

            elif dir_path == PAGES[6]:

                contents, style = self.geneCalc(params)

            elif dir_path == PAGES[7]:

                contents, style = self.geneList(params)

            else:

                raise FileNotFoundError

            response_code = 200

        except FileNotFoundError:
            contents = """
            <html>
                <body>
                    <h1>404 Not Found</h1>
                    <a href="/">Back</a>
                </body>
            </html>
            """

            style = "text/html"
            response_code = 404

        contents = contents.replace("[[lnk]]",LNK)

        encoded_content = contents.encode("utf-8")

        self.send_response(response_code)
        self.send_header("Content-Type",style)

        self.send_header("Content-Length",len(encoded_content))

        self.end_headers()
        self.wfile.write(encoded_content)


socketserver.TCPServer.allow_reuse_address = True

Handler = TestHandler

with socketserver.TCPServer((IP, PORT),Handler) as httpd:

    print(f"Serving at {LNK}")
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nStopped by user")
        httpd.server_close()