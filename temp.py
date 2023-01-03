def crap():
    import requests
    import json

    class Bin2NameClient:
        url = "www.binary2name.com"
        port = 443
        final_url = 'https://' + url + ':' + str(port) + '/'

        def __init__(self, bin_file_path):
            self.bin_file_path = bin_file_path
            self.response = None

        def send_request(self):
            files = {'bin_file': open(self.bin_file_path, 'rb')}
            self.response = requests.post(self.final_url, params=files)

    if __name__ == "__main__":
        bin_file_path = r"C:\Users\snirg\Desktop\ida_exe\bla.txt"
        c = Bin2NameClient(bin_file_path)
        c.send_request()
        print(c.response.text)
        r = json.loads(c.response.text)
        print(r)
        print(type(r))

import requests
import json

url = "www.binary2name.com"
port = 443
final_url = 'https://' + url + ':' + str(port) + '/'

session = requests.Session()
with open(r"C:\Users\snirg\Desktop\ida_exe\notepad++.exe", 'rb') as f:
    form = f
    resp = session.post(final_url, data=form)
session.close()
data = json.loads(resp.text)
print(data)
print(type(data))