import json
import os
from pathlib import Path

GDB_PATH = ""

# Include for vscode autocomplete in unity.h
# ceedling_path = '/var/lib/gems/2.7.0/gems/ceedling-0.31.0'

def vscodeGen_c_cpp_properties(projSett, compSett):
    """
    Generate file .vscode/c_cpp_properties.json
    """
    defines = []
    for d, v in projSett['C_SYMBOLS'].items():
        if not v is None:
            defines.append(str(d) + "=" + str(v))
        else:
            defines.append(str(d))

    browse = []

    try:
        for inc in projSett['C_INCLUDES']:
            i = Path(inc)
            browse.append(str(i.parent))

        browse = list(set(browse))

        components_path = os.getenv('IDF_PATH') + '/components'
        browse.remove(components_path)
        browse.remove(os.getenv('IDF_PATH') + "/components/efuse")
        browse.remove(os.getenv('IDF_PATH') + "/components/esp_wifi")
        browse.append("build/include")
    except:
        pass

    # Change here
    c_cpp_properties = {
        "configurations": [
            {
                'name': 'gcc',
                'defines': defines,
                "compilerPath": compSett['CC'],
                "intelliSenseMode": "linux-gcc-arm",
                "cStandard": "gnu99",
                "cppStandard": "c++17",
                "includePath": projSett['C_INCLUDES'] + ["build/include"],
                "browse": {
                    "path": browse,
                    "limitSymbolsToIncludedHeaders": True,
                    "databaseFilename": "${workspaceFolder}/.vscode/browse.vc.db"
                }
            }
        ],
        "version": 4
    }

    output = json.dumps(c_cpp_properties, indent=4)
    if not os.path.exists('.vscode'):
        os.makedirs('.vscode')
    print("Generate .vscode/c_cpp_properties.json")
    fileout = open(".vscode/c_cpp_properties.json", "w")
    fileout.write("// pymaketool: File autogenerate, see vscode_plugin.py\n")
    fileout.write(output)
    fileout.close()


def vscodeGen_launch(projSett, compSett):
    """
    Generate file .vscode/launch.json
    """
    outputFile = projSett['C_TARGETS']['TARGET']['FILE']
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "cortex-debug",
                "request": "launch",
                "name": "Debug (OpenOCD)",
                "servertype": "openocd",
                "cwd": "${workspaceRoot}",
                "runToMain": True,
                "executable": outputFile,
                "configFiles": [
                    "/SURIX/IPAC/nipac2/Port/WANPAGE_9/WANPAGE_9-Debug.cfg"
                ],
                "gdbPath": GDB_PATH
            }
        ]
    }

    output = json.dumps(launch, indent=4)
    if not os.path.exists('.vscode'):
        os.makedirs('.vscode')
    print("Generate .vscode/launch.json")
    fileout = open(".vscode/launch.json", "w")
    fileout.write("// pymaketool: File autogenerate, see vscode_plugin.py\n")
    fileout.write(output)
    fileout.close()


def vscode_init(projSett, compSett):
    # print(projSett)
    # print(compSett)
    vscodeGen_c_cpp_properties(projSett, compSett)
    # if not Path(GDB_PATH).exists():
    #     print("***GDB not found, edit GDB_PATH in vscode_addon.py")
    #     return
    # vscodeGen_launch(projSett, compSett)
