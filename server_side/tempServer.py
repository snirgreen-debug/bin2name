from http.server import HTTPServer, SimpleHTTPRequestHandler

import ssl

url = 'www.binary2name.com'

cert_path = '/etc/letsencrypt/live/www.binary2name.com/fullchain.pem'

key_path = '/etc/letsencrypt/live/www.binary2name.com/privkey.pem'

httpd = HTTPServer((url, 4443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert_path, keyfile=key_path, server_side=True)

httpd.serve_forever()