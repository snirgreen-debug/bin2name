from http.server import CGIHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

url = 'www.binary2name.com'
serverPort = 4443

cert_path = '/etc/letsencrypt/live/www.binary2name.com/fullchain.pem'

key_path = '/etc/letsencrypt/live/www.binary2name.com/privkey.pem'


class MyServer(CGIHTTPRequestHandler):
    def _predict_binary(self):
        bin_file = self.query_components['bin_file']
        print(bin_file)

    def _parse_components(self):
        query = urlparse(self.path).query
        query_components = query.split("&")
        query_components = [tuple(i.split('=')) for i in query_components]
        self.query_components = {i[0]: i[1] for i in query_components}

    def do_POST(self):
        self._parse_components()
        self._predict_binary()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))


def main():
    webServer = HTTPServer((url, port), MyServer)

    webServer.socket = ssl.wrap_socket(webServer.socket, certfile=cert_path, keyfile=key_path, server_side=True)
    print("Server started http://%s:%s" % (url, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()
