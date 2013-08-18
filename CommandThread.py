from ShellCommander.Helpers import plugin_setting
from ShellCommander.TcpClient import TcpClient
import threading, subprocess

def run_shell_command(command):
    tcp = plugin_setting('tcp')
    if tcp:
        print('run shell command')
        client = TcpClient(tcp['host'], tcp['port'])
        resp = client.send(command)
        return resp
    else:
        resp = subprocess.check_output(command + "; exit 0", shell=True, stderr=subprocess.STDOUT)
        return resp

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
        resp = run_shell_command(self.command)
        self.callback(resp.decode('utf-8'))

    def done(self, callback):
        self.callback = callback
        return self
