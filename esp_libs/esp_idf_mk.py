import sys
import os
from pymakelib import module
from pymakelib.module import getModuleInstance
from pymakelib.module import StaticLibrary
from scripts import esp_cmake

class ESPGeneralComp(module.AbstractModule):
    """
    Compile component of esp32
    """
    def __init__(self, path, component:esp_cmake.ESPComponent):
        super().__init__(path)
        self.component = component
        self.module_name = component.name
        self.name = component.name

    def init(self):
        staticLib = StaticLibrary(name=self.name, outputDir=f"build/{self.name}/", orden=1)
        staticLib.lib_linked = ' '.join(self.component.ldflags)
        staticLib.lib_objs = ""
        staticLib.lib_objs_compile = ""
        staticLib.lib_compile = f"$({staticLib.mkkey}_AR): $({staticLib.mkkey}_OBJECTS)\n\t$(call logger-compile,\"AR\",$@)\n"
        return staticLib

    def getIncs(self):
        return self.component.includes

    def getSrcs(self):
        return None

if not 'clean-all' in sys.argv:
    components = esp_cmake.get_components('build')

    for comp in components:
        @module.ModuleClass
        class ESPModule(ESPGeneralComp):
            def __init__(self, path):
                super().__init__(os.getcwd(), component=comp)