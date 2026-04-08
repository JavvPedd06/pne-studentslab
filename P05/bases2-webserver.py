import http.server
import socketserver
import termcolor
from pathlib import Path

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# Base directory where all HTML files are stored
BASE_PATH = Path("P05/html")

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # 1. Determine which file to serve based on the URL path
        if self.path == "/" or self.path == "/index.html":
            file_path = BASE_PATH / "index.html"
        else:
            # Remove the leading slash to get the relative file path
            filename = self.path.lstrip("/")

        # Construct the full path using pathlib
            file_path = BASE_PATH / filename

        try:
            # 2. Try to open and read the requested file
            contents = file_path.read_text(encoding="utf-8")
            status_code = 200
        except FileNotFoundError:
            # 3. If the file doesn't exist, fallback to error.html
            error_path = BASE_PATH / "error.html"
            contents = error_path.read_text(encoding="utf-8")
            status_code = 404

        # 4. Send HTTP Response
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode('utf-8')))
        self.end_headers()

        # Send the HTML body to the client
        self.wfile.write(contents.encode('utf-8'))


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()