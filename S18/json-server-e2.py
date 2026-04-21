import http.server
import socketserver
import termcolor
from pathlib import Path

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')


        resource = self.path.split('?')[0]

        if resource == "/":
            contents = Path('index.html').read_text()
            content_type = 'text/html'
            error_code = 200
        elif resource == "/listusers":

            contents = Path('people-e1.json').read_text()
            content_type = 'application/json'
            error_code = 200
        else:
            contents = "<h1>404 Not Found</h1>"
            content_type = 'text/html'
            error_code = 404

        self.send_response(error_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))

Handler = TestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()