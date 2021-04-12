import os
import sys
from os.path import basename
from pymakelib import MKVARS
from pymakelib import addon
from pymakelib.eclipse_addon import EclipseAddon
from pymakelib import toolchain as tool
from pymakelib import Define
from scripts import esp_vscode_addon

addon.add(EclipseAddon)
addon.add(esp_vscode_addon.vscode_init)

PROJECT_NAME = basename(os.getcwd())
IDF_PATH = os.getenv('IDF_PATH')

def getProjectSettings():
    return {
        'PROJECT_NAME': basename(os.getcwd()),
        'FOLDER_OUT':   'build/'
    }


def getTargetsScript():
    FOLDER_OUT = 'build/'
    TARGET = FOLDER_OUT + PROJECT_NAME + '.elf'
    TARGET_BIN = FOLDER_OUT + PROJECT_NAME + '.bin'
    BOOTLOADER = FOLDER_OUT + 'bootloader/bootloader.bin'

    TARGETS = {
        'TARGET_32LD': {
            'LOGKEY':  '32LD',
            'FILE':    'build/esp32/esp32.project.ld',
            'SCRIPT':  ['make', '-f', 'esp_idf_project.mk', f'{os.getcwd()}/build/esp32/esp32.project.ld', f'{IDF_PATH}/components/esp32/ld/esp32.project.ld.in']
        },
        'BOOTLOADER': {
            'LOGKEY':  'BOOT',
            'FILE':    BOOTLOADER,
            'SCRIPT': ['make', '-f', 'esp_idf_project.mk', 'bootloader']
        },
        'TARGET': {
            'LOGKEY':  'ELF',
            'FILE':    TARGET,
            'SCRIPT':  [MKVARS.LD, '-o', '$@', MKVARS.OBJECTS, MKVARS.LDFLAGS]
        },
        'TARGET_BIN': {
            'LOGKEY':  'BIN',
            'FILE':    TARGET_BIN,
            'SCRIPT':  ['make', '-f', 'esp_idf_project.mk', f'{os.getcwd()}/build/{PROJECT_NAME}.bin']
        }, 
        'RESUME': {
            'LOGKEY': '>>',
            'FILE': 'APP',
            'SCRIPT': ['@pybuildanalyzer2', TARGET]
        }
    }

    return TARGETS


def getCompilerSet():
    return tool.confGCC('', 'xtensa-esp32-elf-')


LIBRARIES = []

def getCompilerOpts():

    PROJECT_DEF = {
        "ESP_PLATFORM":             None,
        "IDF_VER":                  "v4.4-dev-744-g1cb31e509-dirty",
        "_GNU_SOURCE":              None,
        "UNITY_INCLUDE_CONFIG_H":   None,
        "HAVE_CONFIG_H":            None
    }

    return {
        'MACROS': PROJECT_DEF,
        'MACHINE-OPTS': [
        ],
        'OPTIMIZE-OPTS': [
            '-Os'
        ],
        'OPTIONS': [
            '-Ibuild/include'
        ],
        'DEBUGGING-OPTS': [
            '-ggdb'
        ],
        'PREPROCESSOR-OPTS': [
            '-MP',
            '-MMD'
        ],
        'WARNINGS-OPTS': [
            "-Wall",
            "-Wno-frame-address",
            "-Werror=all", 
            "-Wno-error=unused-function",
            "-Wno-error=unused-but-set-variable", 
            "-Wno-error=unused-variable", 
            "-Wno-error=deprecated-declarations", 
            "-Wextra -Wno-unused-parameter", 
            "-Wno-sign-compare", 
            "-Wno-old-style-declaration",
        ],
        'CONTROL-C-OPTS': [
            "-std=gnu99"
        ],
        'GENERAL-OPTS': [
            "-freorder-blocks",
             "-ffunction-sections",
             "-fdata-sections",
             "-fstrict-volatile-bitfields",
             "-mlongcalls",
             "-nostdlib",
        ],
        'LIBRARIES': LIBRARIES
    }


def getLinkerOpts():
    return [
        "-nostdlib -u call_user_start_cpu0  -Wl,--gc-sections -Wl,-static -Wl,--start-group",
        MKVARS.STATIC_LIBS,
        "-lgcc", 
        "-lstdc++", 
        "-lgcov",
        f"-Wl,--end-group -Wl,-EL -fno-rtti -Wl,-Map=build/{PROJECT_NAME}.map",
    ]
    
