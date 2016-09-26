from threading import Thread, Event

from PyQt4.QtCore import QObject, pyqtSignal


class ThreadMan(QObject):
    onCommandToRun = pyqtSignal()

    def __init__(self):
        self.stop = Event()
        self.thread = Thread()
        self.commands = []

    def kill(self):
        self.stop.set()
        if self.thread is not None:
            self.thread = None

    def run(self, function, *args):
        self.kill()
        self.commands = []
        args = [x for xs in args for x in xs]
        self.stop = Event()
        args.append(self.stop)
        args.append(self.runMain)
        self.thread = Thread(target=function, args=args, name="Thread 2")
        self.thread.daemon = True
        self.thread.start()

    def runMain(self, command, *args):
        self.onCommandToRun.emit()
        self.commands.append((command, args))
