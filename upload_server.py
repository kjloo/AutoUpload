import BaseHTTPServer
from upload_functions import parse_query_string

class RestServer(BaseHTTPServer.HTTPServer):
    def finish_request(self, request, client_address):
        self.storage = self.RequestHandlerClass(request, client_address, self)

class RestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("User Authorized!")
        self.query = parse_query_string(self.path)
