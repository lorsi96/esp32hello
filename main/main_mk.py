from pymakelib import module
from pymakelib.module import StaticLibrary

@module.ModuleClass
class Main(module.BasicCModule):
    
    
    def getIncs(self)->list:
        incs = super().getIncs()
        incs.append('build/include')
        return incs