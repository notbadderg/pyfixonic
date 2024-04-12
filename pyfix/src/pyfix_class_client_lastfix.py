import os
from .utilites import read_txt, read_lastfix


class Client:
    def __init__(self, client_folder, client_ver_file, lastfix_folder, lastfix_file):
        self.folder = client_folder
        self.ver = self._get_version_content(client_ver_file)
        self.lastfix = Lastfix(lastfix_folder, lastfix_file)

    @staticmethod
    def _get_version_content(client_ver_file):
        if os.path.exists(client_ver_file):
            return read_txt(client_ver_file)
        else:
            return None


class Lastfix:
    def __init__(self, folder, file):
        self.folder = folder
        self.file = file
        self.ver = None
        self.fix = None
        self._get_lastfix_content()

    def _get_lastfix_content(self) -> None:
        if os.path.exists(self.file):
            lastfix_content = read_lastfix(self.file)
            self.ver = lastfix_content['Version']
            self.fix = lastfix_content['Fix']
