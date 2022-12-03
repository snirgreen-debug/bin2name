import http.server, ssl, socketserver

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("/etc/letsencrypt/live/www.binary2name.com/privkey.pem")
server_addr = ("132.69.8.16", 443)

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(server_addr, handler) as hpd:
    hpd.socket = context.wrap_socket(hpd.socket, serverside=True)
    hpd.server_forever()
