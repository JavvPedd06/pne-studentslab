#ADD THE ENDPOINT /geneReverse
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
PATH = "html notes"
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
    "/geneList",
    "/geneReverse"
]

env = Environment(loader=FileSystemLoader(PATH))  # This part creates the jinja enviroment.


class TestHandler(http.server.BaseHTTPRequestHandler):
    # THIS IS THE FUNCTION I USE TO CONNECT WITH ENSEMBL.
    # 1st creates a connection conn = http.client.HTTPSConnection(SERVER)
    # It sends a GET request conn.request("GET", endpoint, headers=headers)
    # Recieves a positive response if everything is working
    # the json.loads(response.read().decode())
    # Does 3 things:
    # -Read the bytes of the response .read()
    # -Turn the bytes into a string .decode()
    # -Load the json string into a dictionary .loads()
    def get_ensembl_data(self, endpoint):
        conn = http.client.HTTPSConnection(SERVER)
        headers = {"Content-Type": "application/json"}
        conn.request("GET", endpoint, headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read().decode())
        return None

    # This function checks if the user wants a JSON information (For the advanced part)
    def wants_json(self, params):
        return params.get("json") == "1"

    # This function get a list of species from ensembl using the previous function data = self.get_ensembl_data("/info/species")
    # From the data, then the species are extracted
    # The limit is extracted from the info the user provides.ç
    # In case the user wants the json then it is dumped into a dictionary.
    # The html notes part returns the information loading the template called list.html notes (stored in the folder...) THE JINJA THING
    def listSpecies(self, params):
        data = self.get_ensembl_data("/info/species")
        species_list = data.get("species", []) if data else []
        limit = int(params.get("limit", 0))
        if limit > 0:
            species_list = species_list[:limit]
        result = {"species": species_list}
        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("list.html notes").render(species_list=species_list)
        return html, "text/html notes"

    # This function gets the karyotype using the function get_ensembl
    # Same idea as before
    # The params thing is obtained by the GET function (At the very end)
    def karyotype(self, params):
        species = params.get("species", "")
        data = self.get_ensembl_data(f"/info/assembly/{species}")
        karyotype = data.get("karyotype", []) if data else []
        result = {
            "species": species,
            "karyotype": karyotype}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("karyotype.html notes").render(species=species, karyotype=karyotype)
        return html, "text/html notes"

    # THIS function obtains the length of the desired chromosome
    # With the params the species and the chromosome is obtained
    # The data in ensmbl is sotred in regions.
    # the interesting region here is top_level_data. If it exists for each region in the top_region it looks for the name part which is associated with a chromosome
    # If the name of the chromosomes is the same as the one stored, the length stored is the one associated
    # the post-processing is the same.
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

        html = env.get_template("length.html notes").render(species=species, chromo=chromo, length=length)
        return html, "text/html notes"

    # This function obtains the Id of a gene
    # If the data type is == gene then the id is found
    # The result is stored in a dictionary
    def geneLookup(self, params):
        gene = params.get("gene", "")
        data = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")

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

        html = env.get_template("geneLookup.html notes").render(gene=gene, gene_id=gene_id)
        return html, "text/html notes"

    # This obtains the sequence of a gene
    # It firstly obtains the id of a gene just like before
    # If the gene id is found then it looks for the sequence. Creating the seq_data variable which contains a lot of data
    # Then the final sequence is the seq part of the seq_data
    # Jsut like in the previous one, the data is stored in a dictionary
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
            "sequence": sequence
        }

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneSeq.html notes").render(gene=gene, gene_id=gene_id, sequence=sequence)
        return html, "text/html notes"

    # This function get the key info a gene
    # The parameter input is the gene name.
    # with the get.() starts looking for the data in particular need
    # The length is manually calculated
    # Evreything is stored in a dict which is then put inside another one
    def geneInfo(self, params):
        gene = params.get("gene", "")
        data = self.get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene}?expand=1")

        if not data:
            data = {}

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
            "length": length}

        result = {"gene": gene, "info": info}

        if self.wants_json(params):
            return json.dumps(result), "application/json"
        html = env.get_template("geneInfo.html notes").render(gene=gene, info=info)

        return html, "text/html notes"

    # This function is quite complicated, it calculates everything
    # Firstly it makes sure that the gene_id and the seq_data exist
    # Then, using the seq class, computes the info of the sequence obtained in sequence = seq_data["seq"].upper()
    # The info is stored in a dictionary
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
            result = {"gene": gene, "error": "Gene not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html notes").render(gene=gene, error="Gene not found")
            return html, "text/html notes"

        seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")

        if not seq_data or "seq" not in seq_data:
            result = {"gene": gene, "error": "Sequence not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html notes").render(gene=gene, error="Sequence not found")

            return html, "text/html notes"

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

        html = env.get_template("geneCalc.html notes").render(gene=gene, gene_id=gene_id, length=length, a=a_pct, c=c_pct,
                                                        g=g_pct, t=t_pct)

        return html, "text/html notes"

    # This get all the genes in a chromosome region
    # It saves the name and id as well as the chromosome, start and endpoint (Inputed by the user)
    def geneList(self, params):
        chromo = params.get("chromo", "")
        start = params.get("start", "")
        end = params.get("end", "")
        genes = []
        if chromo and start and end:
            data = self.get_ensembl_data(f"/overlap/region/human/{chromo}:{start}-{end}?feature=gene")

            if data:
                for item in data:
                    gene_name = item.get("external_name")
                    gene_id = item.get("id")
                    if gene_name:
                        genes.append({"name": gene_name, "id": gene_id})

        result = {
            "chromosome": chromo,
            "start": start,
            "end": end,
            "genes": genes}

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneList.html notes").render(chromo=chromo, start=start, end=end, genes=genes)
        return html, "text/html notes"
    def geneReverse(self,params):
        gene = params.get("gene", "")

        lookup = self.get_ensembl_data(f"/xrefs/symbol/homo_sapiens/{gene}")

        gene_id = None
        if lookup:
            for item in lookup:
                if item.get("type") == "gene":
                    gene_id = item.get("id")
                    break

        if not gene_id:
            result = {"gene": gene, "error": "Gene not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html notes").render(gene=gene, error="Gene not found")
            return html, "text/html notes"

        seq_data = self.get_ensembl_data(f"/sequence/id/{gene_id}")

        if not seq_data or "seq" not in seq_data:
            result = {"gene": gene, "error": "Sequence not found"}

            if self.wants_json(params):
                return json.dumps(result), "application/json"

            html = env.get_template("geneCalc.html notes").render(gene=gene, error="Sequence not found")

            return html, "text/html notes"

        sequence = seq_data["seq"].upper()
        seq = Seq(sequence)
        reverse_seq = seq.reverse()

        result = {
            "gene": gene,
            "gene_id": gene_id,
            "sequence": sequence,
            "reverse": reverse_seq
        }

        if self.wants_json(params):
            return json.dumps(result), "application/json"

        html = env.get_template("geneReverse").render(gene=gene, gene_id = gene_id, sequence = sequence, reverse=reverse_seq)
        return html, "text/html notes"



    # THIS IS THE KEY METHOD
    # The parsed thing splits the URL
    # params = {k: v[0]for k, v in parse_qs(parsed_url.query).items()}
    # -It converts the URL parameters into a normal Python dictionary.
    # -Basically the function converts query parameters into a dictionary.
    # The final params basically turns something like:
    # params = {
    #     "gene": "BRCA2",
    #     "json": "1"
    # } WHICH IS SOMETHING USEFUL
    def do_GET(self):
        print("GET received!")
        termcolor.cprint("  " + self.requestline, "green")
        parsed_url = urlparse(self.path)
        dir_path = parsed_url.path
        params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        # THIS IS THE ROUTING, it controls what is executed
        try:

            if dir_path == "/" or dir_path == "/index2.html notes":
                contents = env.get_template("index2.html notes").render()
                style = "text/html notes"

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
            elif dir_path == PAGES[8]:

                contents, style = self.geneReverse(params)

            else:

                raise FileNotFoundError

            response_code = 200

        except FileNotFoundError:
            contents = """
            <html notes>
                <body>
                    <h1>404 Not Found</h1>
                    <a href="/">Back</a>
                </body>
            </html notes>
            """

            style = "text/html notes"
            response_code = 404

        # This is where everything is encoded.
        # this is where the data is send. THis is what the dreams are made of
        contents = contents.replace("[[lnk]]", LNK)
        encoded_content = contents.encode("utf-8")
        self.send_response(response_code)

        self.send_header("Content-Type", style)
        self.send_header("Content-Length", len(encoded_content))

        self.end_headers()
        self.wfile.write(encoded_content)


socketserver.TCPServer.allow_reuse_address = True

Handler = TestHandler

with socketserver.TCPServer((IP, PORT), Handler) as httpd:
    print(f"Serving at {LNK}")
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nStopped by user")
        httpd.server_close()