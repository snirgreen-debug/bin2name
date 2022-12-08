import idaapi
import ida_nalt
import requests


# import idautils
# import ida_bytes
# import ida_diskio
# import idc
# import operator
# import os
# import glob


class Bin2NameClient:
    url = "www.binary2name.com"
    port = 4443
    final_url = 'https://' + url + ':' + str(port) + '/'

    def __init__(self, bin_file_path):
        self.bin_file_path = bin_file_path

    def send_request(self):
        files = {'bin_file': open('test_file.txt', 'rb')}
        self.response = requests.post(self.final_url, params=files)


class bin2name(idaapi.plugin_t):
    comment = "todo"
    help = "todo"
    wanted_name = "Binary2Name"
    wanted_hotkey = "Ctrl-Shift-B"
    flags = idaapi.PLUGIN_KEEP

    def init(self):
        idaapi.attach_action_to_menu("Search", "Binary2Name", idaapi.SETMENU_APP)

        self.bin_file_path = ida_nalt.get_input_file_path()
        self.client = Bin2NameClient(self.bin_file_path)

        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, arg):
        print("hello, the file path is: ")
        print(self.client.bin_file_path)


# register IDA plugin
def PLUGIN_ENTRY():
    return bin2name()
