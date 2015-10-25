#encoding=utf8
import json
import os
import subprocess
from wox import Wox
from os import listdir
from os.path import isfile, join, isdir


class XShell(Wox):

    def load_session(self, session_path):
        files = []
        for f in listdir(session_path):
            if isfile(join(session_path, f)) and not f.endswith("ini"):
                files.append({'f': f, 'd': session_path})
            if isdir(join(session_path, f)):
                files = files + self.load_session(join(session_path, f))
        return files

    def query(self, query):
        with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as content_file:
            config = json.loads(content_file.read())
        session_path = config["SessionPath"]
        sessions = self.load_session(session_path)
        res = []
        for p in sessions:
            if query in p['f']:
                res.append({"Title": p['f'].replace(".xsh", ""), "IcoPath": "terminal.ico", "JsonRPCAction": {
                           "method": "open_session", "parameters": [p['d'].replace("\\", "\\\\"), p['f']]}})
        return res

    def open_session(self, folder, session):
        #self.debug(join(folder,session))
        subprocess.call('{}'.format(
            join(folder.encode('gbk'), session.encode('gbk'))), shell=True)

if __name__ == "__main__":
    XShell()
