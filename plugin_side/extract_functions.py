import idaapi
import ida_nalt
import ida_funcs
import idautils
import idc
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
        for segea in idautils.Segments():
            for funcea in idautils.Functions(segea, idc.SegEnd(segea)):
                functionName = idc.GetFunctionName(funcea)
                for (startea, endea) in idautils.Chunks(funcea):
                    for head in idautils.Heads(startea, endea):
                        print(functionName, ":", "0x%08x" % (head), ":", idautils.GetDisasm(head))
        print("done!")


# register IDA plugin
def PLUGIN_ENTRY():
    return FuncExtract()

