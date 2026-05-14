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
GENE_DIR = "./sequences/"
LNK = f"http://{IP}:{PORT}"
SERVER = "rest.ensembl.org"
PAGES = ["/listSpecies", "/karyotype", "/chromosomeLength"]
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
            else:
                raise FileNotFoundError

            response_code = 200
        except FileNotFoundError:
            # Fallback 404
            contents = "<html><body><h1>404 Not Found</h1><a href='/'>Back</a></body></html>"
            style = "text/html"
            response_code = 404

        # Replace the placeholder for the main link
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