import inspect

import mods


class modloader():

    def __init__(self):
        self.SinitL = []
        self.CinitL = []
        self.messageL = []
        self.newidL = []
        self.ScloseL = []
        self.CcloseL = []
        for i in mods.__all__:
            for j, k in inspect.getmembers(getattr(mods, i), predicate=inspect.isfunction):
                for l, m in [(self.SinitL, "Sinit"), (self.CnitL, "Cinit"), (self.messageL, "message"),
                             (self.newidL, "newid"), (self.ScloseL, "Sclose"), (self.CcloseL, "Cclose")]:
                    if j == m:
                        l.append(k)
                        break

    def Sinit(self, server):
        for i in self.SinitL:
            i(server)

    def Cinit(self, client, server):
        for i in self.CinitL:
            i(client, server)

    def message(self, client, server):
        for i in self.messageL:
            i(client, server)
            
    def newid(self, client, server):
        for i in self.newidL:
            i(client, server)

    def Sclose(self, server):
        for i in self.ScloseL:
            i(server)

    def Cclose(self, client, server):
        for i in self.CcloseL:
            i(client, server)       