from pathlib import Path
import sys
import os
import subprocess

class ESPComponent:

    def __init__(self, path, outputDir, idf_path=os.getenv('IDF_PATH')):
        self.idf_path = idf_path
        self.outputDir = Path(outputDir)
        self.path = Path(path).parent
        self.name = self.path.name
        self.isempty = False
        self.includes = []
        self.ldflags = []
        self.linker_deps = []
        self.submodules = []
        self.libraries = []
        self.ldfragments = []
        replaces = {
            '$(IDF_PATH)': self.idf_path,
            '$(BUILD_DIR_BASE)': str(self.outputDir)
        }
        comp_var_mk = open(self.outputDir / Path(self.name) / Path('component_project_vars.mk'))
        for line in comp_var_mk:
            if line.startswith("COMPONENT_INCLUDES"):
                self.includes.extend(self.__get_var_make_from_line(line, "COMPONENT_INCLUDES", replaces=replaces))
            elif line.startswith("COMPONENT_LDFLAGS"):
                self.ldflags.extend(self.__get_var_make_from_line(line, "COMPONENT_LDFLAGS", replaces=replaces))
            elif line.startswith("COMPONENT_LINKER_DEPS"):
                self.linker_deps.extend(self.__get_var_make_from_line(line, "COMPONENT_LINKER_DEPS", replaces=replaces))
            elif line.startswith("COMPONENT_SUBMODULES"):
                self.submodules.extend(self.__get_var_make_from_line(line, "COMPONENT_SUBMODULES", replaces=replaces))
            elif line.startswith("COMPONENT_LIBRARIES"):
                self.libraries.extend(self.__get_var_make_from_line(line, "COMPONENT_LIBRARIES", replaces=replaces))
            elif line.startswith("COMPONENT_LDFRAGMENTS"):
                self.ldfragments.extend(self.__get_var_make_from_line(line, "COMPONENT_LDFRAGMENTS", replaces=replaces))
        
        if not self.includes and not self.ldflags:
            self.isempty = True

    def __get_var_make_from_line(self, line, varname, replaces={}):
        for k, v in replaces.items():
            if k in line:
                line = line.replace(k, v)
        value = str(line).split(" += ")[1].split()
        return value

    def get_includes(self):
        return self.includes

def get_components(outputDir, jobs=os.cpu_count()):
    subprocess.run(['make', '-j', str(jobs), '-f', 'esp_idf_project.mk', f'{os.getcwd()}/build/ldgen_libraries'])
    components = []
    ldgen_libraries = open(Path(outputDir) / Path('ldgen_libraries'), "r")
    for line in ldgen_libraries:
        lib = Path(line.strip())
        components.append(ESPComponent(lib, outputDir))
    return components

# comps = get_components('build')

# for c in comps:
#     print(c.name)
#     print("\t"+str(c.includes))
#     print("\t"+str(c.ldflags))
#     print("\t"+str(c.linker_deps))
#     print("\t"+str(c.submodules))
#     print("\t"+str(c.libraries))
#     print("\t"+str(c.ldfragments))
