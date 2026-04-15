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

        termcolor.cprint(self.requestline, 'green')


        parsed_url = urlparse(self.path)
        path = parsed_url.path
        arguments = parse_qs(parsed_url.query)


        if path == "/":

            try:
                response_content = Path('html/form-1.html').read_text()
                status_code = 200
            except FileNotFoundError:
                response_content = "Error: html/index.html not found."
                status_code = 404

        elif path == "/echo":

            message = arguments.get('msg', [''])[0]

            response_content = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Message:</title></head>
            <body>
                <h1>Echo Server Response</h1>
                <p><strong>{message}</strong></p>
                <a href="/">Return to the main form</a>
            </body>
            </html>
            """
            status_code = 200

        else:
            template = Path('html/error.html').read_text()
            response_content = template.replace("{{path}}", path)
            status_code = 404


        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')

        response_bytes = response_content.encode('utf-8')
        self.send_header('Content-Length', len(response_bytes))
        self.end_headers()
        self.wfile.write(response_bytes)


# ------------------------
# Server MAIN program
# ------------------------
Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()
