import sys

class StdoutConsole(object):

    def __init__(self):
        self.out = sys.stdout

    def write(self, msg):
        self.out.write(msg + os.linesep)
