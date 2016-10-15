import datetime
from os import path, makedirs, walk


class History(object):
    def __init__(self):
        self.fileOpen = False
        self.fileObj = None
        self.fileArray = []
        self.fileNum = 0
        self.db = []
        self._updateDb()

    def getLast50(self):
        output = []
        last = "all"
        for i in reversed(self.db):
            if i.strip() != "":
                i = i.replace("\n", "")
                if i != self._fileName() or not self.fileOpen:
                    f = open(i, "r")
                    output += f.readlines()
                    f.close()
                else:
                    output += self.fileArray
                if len(output) > 50:
                    last = i
                    break
        return last, "".join(output)

    def get50More(self, last_file):
        output = []
        last = "all"
        start = list(reversed(self.db)).index(last_file) + 1
        for i in list(reversed(self.db))[start:]:
            if i.strip() != "":
                i = i.replace("\n", "")
                if i != self._fileName() or not self.fileOpen:
                    f = open(i, "r")
                    output += f.readlines()
                    f.close()
                else:
                    output += self.fileArray
                if len(output) > 50:
                    last = i
                    break
        return last, "".join(output)

    def _updateDb(self):
        self.db = []
        for root, _, files in walk("chat/Main"):
            for name in files:
                if name != "welcome.chat":
                    self.db.append(path.join(root, name))
        self.db.sort()

    def _fileName(self):
        return "chat/Main/" + str(datetime.date.today()).replace("-", "/") + "/" + str(self.fileNum) + ".chat"

    def add(self, text):  # To add text to the history
        if not path.isfile(self._fileName()):  # If file dose not exist make it
            self.fileNum = 0
            self.fileArray = []
            self.fileOpen = True
            folders = "chat/Main/"
            for i in str(datetime.date.today()).split("-"):
                folders += i + "/"
                if not path.exists(folders):
                    makedirs(folders)
            try:
                self.fileObj.close()
            except AttributeError:
                pass
            self.fileObj = open(self._fileName(), "w")
            self._updateDb()
        elif not self.fileOpen:
            self.fileOpen = True
            f = open(self._fileName(), "r")
            self.fileArray = f.readlines()
            f.close()
            self.fileObj = open(self._fileName(), "a")
        if len(self.fileArray) >= 50:
            self.fileNum += 1
            self.fileArray = []
            self.fileObj.close()
            self.fileObj = open(self._fileName(), "w")
            self._updateDb()
        self.fileArray.append(text + "\n")  # Add text to string
        self.fileObj.write(text + "\n")  # Add t
        # ext to file
