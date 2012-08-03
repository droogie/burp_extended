import os
import imp
import inspect
import Extension

def getExtensionClassList():
    moduleDict = {}
    classTools = []
    #(\/)(*;;;;*)(\/) - zoidberg will find all your extensions for you.
    for r,d,f in os.walk("lib/extensions/"):
        for files in f:
            if files.endswith(".py"):
                 path = os.path.join(r,files)
                 moduleDict[path] = imp.load_source(files[:-3], path)
                 members = inspect.getmembers(moduleDict[path], lambda m:inspect.isclass(m))
                 for name, member in members:
                    if member != Extension.Extension and issubclass(member, Extension.Extension):
                        classTools.append(member)

    return classTools
