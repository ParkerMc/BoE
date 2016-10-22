import fileinput
import sys

def replaceAll(file):
    searchExp = "uic.loadUiType(path.join(path.dirname(path.realpath(__file__))"
    replaceExp = "uic.loadUiType(path.join(path.dirname(path.realpath(__file__))[:-10]"
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)
for i in ["error.py", "AddServer.py", "CreateUser.py", "gui.py", "Login.py", "ServerList.py"]:
    replaceAll("../../Client-Python/"+i)
