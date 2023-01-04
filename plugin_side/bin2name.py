import idaapi
import ida_nalt
import requests
import json


# import idautils
# import ida_bytes
# import ida_diskio
# import idc
# import operator
# import os
# import glob


class Bin2NameClient:
    url = "www.binary2name.com"
    port = 443
    final_url = 'https://' + url + ':' + str(port) + '/'

    def __init__(self, bin_file_path):
        self.bin_file_path = bin_file_path
        self.response = None

    def send_request(self):
        session = requests.Session()
        with open(self.bin_file_path, 'rb') as bin_file:
            self.response = session.post(self.final_url, data=bin_file)


class bin2name(idaapi.plugin_t):
    comment = "todo"
    help = "todo"
    wanted_name = "Binary2Name"
    wanted_hotkey = "Ctrl-Shift-B"
    flags = idaapi.PLUGIN_KEEP

    def _parse_client_response(self):
        response = self.client.response.text
        response = json.loads(response)
        return response

    def init(self):
        idaapi.attach_action_to_menu("Search", "Binary2Name", idaapi.SETMENU_APP)

        self.bin_file_path = ida_nalt.get_input_file_path()
        self.client = Bin2NameClient(self.bin_file_path)

        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, _):
        self.client.send_request()
        addr_name_map = self._parse_client_response()
        for addr, name in addr_name_map.items():
            idaapi.set_name(int(addr, 16), name)

        print("done!")


# register IDA plugin
def PLUGIN_ENTRY():
    return bin2name()

