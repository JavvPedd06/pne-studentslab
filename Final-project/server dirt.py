import http.server
import socketserver
import termcolor
import requests
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, FileSystemLoader

# Define the Server's port
PORT = 8080
socketserver.TCPServer.allow_reuse_address = True


env = Environment(loader=FileSystemLoader('html'))


class EnsemblHandler(http.server.BaseHTTPRequestHandler):

    def get_ensembl_data(self, endpoint):
        url = f"https://rest.ensembl.org{endpoint}"
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"})
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def render_template(self, template_name, context):
        template = env.get_template(template_name)
        return template.render(context)

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        args = parse_qs(parsed_url.query)

        status_code = 200
        content = ""

        try:
            # --- MAIN ENDPOINT ---
            if path == "/":
                content = self.render_template('index.html', {})

            # --- LIST SPECIES ---
            elif path == "/list":
                data = self.get_ensembl_data("/info/species")
                limit_arg = args.get('limit', [None])[0]
                limit = int(limit_arg) if limit_arg and limit_arg.isdigit() else None

                species_list = data.get('species', []) if data else []
                if limit:
                    species_list = species_list[:limit]

                content = self.render_template('list.html', {'species_list': species_list})

            # --- KARYOTYPE ---
            elif path == "/karyotype":
                species = args.get('species', [''])[0]
                data = self.get_ensembl_data(f"/info/assembly/{species}")
                karyotype = data.get('karyotype', []) if data else []
                content = self.render_template('karyotype.html', {'species': species, 'karyotype': karyotype})

            # --- CHROMOSOME LENGTH ---
            elif path == "/chromosomeLength":
                species = args.get('species', [''])[0]
                chromo = args.get('chromo', [''])[0]
                data = self.get_ensembl_data(f"/info/assembly/{species}")

                length = None
                if data and 'top_level_region' in data:
                    for region in data['top_level_region']:
                        if region['name'] == chromo:
                            length = region['length']
                            break

                content = self.render_template('length.html', {
                    'species': species,
                    'chromo': chromo,
                    'length': length
                })

            else:
                status_code = 404
                content = "<html><body><h1>404 Not Found</h1><a href='/'>Back</a></body></html>"

        except Exception as e:
            status_code = 500
            content = f"<html><body><h1>Server Error</h1><p>{str(e)}</p></body></html>"

        # Response handling
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        res_bytes = content.encode('utf-8')
        self.send_header('Content-Length', len(res_bytes))
        self.end_headers()
        self.wfile.write(res_bytes)


# Server MAIN program
with socketserver.TCPServer(("", PORT), EnsemblHandler) as httpd:
    termcolor.cprint(f"Serving Ensembl App at PORT {PORT}", 'blue')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()