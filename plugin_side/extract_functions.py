import idaapi
import ida_nalt
import ida_funcs
import requests
import json
import re


class FuncExtract(idaapi.plugin_t):
    comment = "todo"
    help = "todo"
    wanted_name = "FuncExtract"
    wanted_hotkey = "Ctrl-Shift-L"
    flags = idaapi.PLUGIN_KEEP

    def _parse_client_response(self):
        response = self.client.response.text
        response = json.loads(response)
        return response

    def init(self):
        idaapi.attach_action_to_menu("Search", "FuncExtract", idaapi.SETMENU_APP)

        self.bin_file_path = ida_nalt.get_input_file_path()
        self.pattern = re.compile("sub_[0123456789ABCDEFabcdef]+")

        return idaapi.PLUGIN_KEEP

    def term(self):
        pass

    def run(self, _):
        addr_name_map = self._parse_client_response()
        for addr, name in addr_name_map.items():
            addr = int(addr)
            func_name = ida_funcs.get_func_name(addr)
            if func_name and re.match(self.pattern, func_name):
                func_ptr = ida_funcs.get_func(addr)
                current_cmt = ida_funcs.get_func_cmt(func_ptr, False)
                current_cmt = current_cmt + '\n' if current_cmt else ''
                ida_funcs.set_func_cmt(func_ptr, current_cmt+f"{name}", False)
                print(f"{addr}: {name} - Name already exists. Added as a comment.")
            else:
                idaapi.set_name(addr, name)
                print(f"{addr}: {name} - Name changed.")

        print("done!")


# register IDA plugin
def PLUGIN_ENTRY():
    return FuncExtract()

