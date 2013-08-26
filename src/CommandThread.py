import threading
import subprocess


class CommandThread(threading.Thread):
    count = 0

    def __init__(self, command):
        threading.Thread.__init__(self)
        CommandThread.count += 1
        count = CommandThread.count

        self.threadID = count
        self.name = "thread-%d" % (count)
        self.command = command

    def run(self):
        resp = subprocess.check_output(self.command + "; exit 0", shell=True, stderr=subprocess.STDOUT)
        self.callback(resp.decode('utf-8'))

    def done(self, callback):
        self.callback = callback
        return self
