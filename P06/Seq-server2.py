import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Define the Server's port
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Log the request to the terminal in green
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        path = parsed_url.path
        arguments = parse_qs(parsed_url.query)

        # ---------------------------------------------------------------------
        # 1. Main Page
        # ---------------------------------------------------------------------
        if path == "/":
            try:
                response_content = Path('html/operations.html').read_text()
                status_code = 200
            except FileNotFoundError:
                response_content = "Error: html/gene.html not found."
                status_code = 404

        # ---------------------------------------------------------------------
        # 2. Ping Service
        # ---------------------------------------------------------------------
        elif path == "/ping":
            response_content = """
            <html>
            <head><title>Ping Status</title></head>
            <body>
                <h1 style="color: green;">The server is alive!</h1>
                <hr>
                <a href="/">Return to the main page</a>
            </body>
            </html>
            """
            status_code = 200

        # ---------------------------------------------------------------------
        # 3. Get Service (Sequence by Number)
        # ---------------------------------------------------------------------
        elif path == "/get":
            num_selected = arguments.get('num', ['0'])[0]
            try:
                count = int(num_selected)
                base_dna = "AGCTTCGATCGACTAGCTAGCTAGCATATCGGCTAT"
                dna_string = (base_dna + " ") * (count + 1)
            except ValueError:
                dna_string = "Invalid selection"

            response_content = f"""
            <html>
            <head><title>Sequence {num_selected}</title></head>
            <body>
                <h1>Sequence Number: {num_selected}</h1>
                <p style="word-break: break-all;">{dna_string}</p>
                <hr>
                <a href="/">Return to the main page</a>
            </body>
            </html>
            """
            status_code = 200

        # ---------------------------------------------------------------------
        # 4. Gene Service (Reading from files in P06-server&sequences)
        # ---------------------------------------------------------------------
        elif path == "/gene":
            gene_name = arguments.get('name', [''])[0]

            # Update folder path as discussed: P06-server&sequences
            genes_db = {
                "U5": "./P06-server&sequences/U5.txt",
                "ADA": "./P06-server&sequences/ADA.txt",
                "FRAT1": "./P06-server&sequences/FRAT1.txt",
                "FXN": "./P06-server&sequences/FXN.txt",
                "RNU6_269P": "./P06-server&sequences/RNU6_269P.txt"
            }

            file_path = genes_db.get(gene_name)
            if file_path:
                try:
                    sequence = Path(file_path).read_text().strip()
                    status_code = 200
                except FileNotFoundError:
                    sequence = f"Error: File for {gene_name} not found."
                    status_code = 404
            else:
                sequence = "Gene not found."
                status_code = 404

            response_content = f"""
            <html>
            <head><title>Gene: {gene_name}</title></head>
            <body>
                <h1>Gene Result: {gene_name}</h1>
                <p style="word-break: break-all; font-family: monospace;">{sequence}</p>
                <hr>
                <a href="/">Return to the main page</a>
            </body>
            </html>
            """

        # ---------------------------------------------------------------------
        # 5. Operation Service (Handling 3 specific buttons)
        # ---------------------------------------------------------------------
        elif path == "/operation":
            seq = arguments.get('seq', [''])[0].upper()
            op = arguments.get('op', [''])[0]

            result = ""
            title = ""

            if op == "info":
                title = "Sequence Information"
                length = len(seq)
                a, t, g, c = seq.count('A'), seq.count('T'), seq.count('G'), seq.count('C')
                result = f"Length: {length}<br>A: {a}<br>T: {t}<br>G: {g}<br>C: {c}"

            elif op == "complement":
                title = "Complement Sequence"
                comp_map = str.maketrans("ATGC", "TACG")
                result = seq.translate(comp_map)

            elif op == "reverse":
                title = "Reverse Sequence"
                result = seq[::-1]

            response_content = f"""
            <html>
            <head><title>{title}</title></head>
            <body>
                <h1>{title}</h1>
                <p><strong>Original:</strong> {seq}</p>
                <p><strong>Result:</strong> {result}</p>
                <hr>
                <a href="/">Return to the main page</a>
            </body>
            </html>
            """
            status_code = 200

        # ---------------------------------------------------------------------
        # 6. 404 Handler
        # ---------------------------------------------------------------------
        else:
            status_code = 404
            response_content = "<html><body><h1>404 Not Found</h1><a href='/'>Back</a></body></html>"

        # Final Header and Writing
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        response_bytes = response_content.encode('utf-8')
        self.send_header('Content-Length', len(response_bytes))
        self.end_headers()
        self.wfile.write(response_bytes)


# Server MAIN program
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()