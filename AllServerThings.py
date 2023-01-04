from http.server import CGIHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import subprocess
import json
import time


url = 'www.binary2name.com'
port = 443
serverPort = port
cert_path = '/etc/letsencrypt/live/www.binary2name.com/fullchain.pem'
key_path = '/etc/letsencrypt/live/www.binary2name.com/privkey.pem'

EXE_FILE_PATH = "./our_dataset/nero_ds/"
LOF_FILE_PATH = "./nero/models_9999_log.txt"


class MyServer(CGIHTTPRequestHandler):
    
    def _predict_binary(self):
        print(bin_file[:100])
        # PredictWrapper.SaveBinFile(bin_file)

    def _parse_components(self):
        query = urlparse(self.path).query
        query_components = query.split("&")
        query_components = [tuple(i.split('=')) for i in query_components]
        self.query_components = {i[0]: i[1] for i in query_components}

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))

        timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
        filename = EXE_FILE_PATH+timestr+".exe"

        f = open("demofile.exe", "ab") # change to filename
        for i in range(content_length//1024):
            buffer = self.rfile.read(1024)
            print(buffer[:10])
            f.write(buffer)

        buffer = self.rfile.read(content_length%1024)
        print(buffer[:10])
        f.write(buffer)
        
        f.close()
        print("end of while")
        my_dict = {"10016BA" : "my_func"}
        body = json.dumps(my_dict).encode()
        # self._parse_components()
        # self._predict_binary()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)


class PredictWrapper:
    def __init__(self):
        self.name = "name"
        self.LogParser = LogParser()

    def SaveBinFile(self, bin_file):
        exe_folder_path = "our_dataset/nero_ds/"
        with open(exe_folder_path, 'wb') as f:
            f.write(bin_file)

    def Predict(self):
        predict_file_name = "./run_pipeline_for_predict.sh"
        rc = subprocess.call(predict_file_name, shell=True)
        
        # Get the full Log Path
        path = "models_9999_log.txt"
        address2name = self.LogParser.Parse(path)
        return address2name

class LogParser:
    def __init__(self):
        self.name = "name"
    def Parse(self, path):
        address2name = {}
        file = open(path, 'r')
        lines = file.readlines()
        for line in lines[1:]:
            tokens = line.split(',')
            address = tokens[1].split('@')[0]
            predictedName = tokens[3]
            if not (predictedName == ""):
                address2name[address] = predictedName
        return address2name


if __name__ == '__main__':
    # connecting to server
    webServer = HTTPServer((url, port), MyServer)

    webServer.socket = ssl.wrap_socket(webServer.socket, certfile=cert_path, keyfile=key_path, server_side=True)
    print("Server started http://%s:%s" % (url, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
