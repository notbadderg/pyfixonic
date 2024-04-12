import ipaddress
import os
import shutil
import socket
import sys
from .pyfix_class_client_lastfix import client, Lastfix
from .utilites import get_date_for_folder_name
from .pythonping import ping


class Server:
    def __init__(self, cumulative_folder, cumulative_lastfix_file, ws_list_file,
                 test_ws_list_file, pyfix_temp_folder):
        self.cumulative_folder = cumulative_folder
        self.cumulative_lastfix_file = cumulative_lastfix_file
        self.ws_list_file = ws_list_file
        self.test_ws_list_file = test_ws_list_file
        self.pyfix_temp_folder = pyfix_temp_folder

        self.cur_package = None
        self.cur_lastfix = None

    def _clean_pyfix_temp(self, count=2) -> None:
        dirs = os.listdir(self.pyfix_temp_folder)
        dirs.sort(reverse=True)
        dirs = dirs[count:]
        for dir_ in dirs:
            path = os.path.join(self.pyfix_temp_folder, dir_)
            try:
                shutil.rmtree(path)
            except PermissionError:
                sys.exit('\033[91mОтказано в доступе !\033[0m')

    def prepare_package(self):
        self._clean_pyfix_temp()
        package_name = get_date_for_folder_name()
        # Client
        src = self.cumulative_folder
        dst = os.path.join(self.pyfix_temp_folder, package_name, 'XXXXXX', 'Client')
        if not os.path.exists(src):
            sys.exit(f'\033[91m! Не найден кумулятивный пакет {src} (не выполнено дистрибутивование?)\033[0m')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        # Lastfix
        src = self.cumulative_lastfix_file
        dst = os.path.join(self.pyfix_temp_folder, package_name, 'XXXXXX_lastfix')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        shutil.copy(src, dst+'\\lastfix_pyfix.csv')

        self.cur_package = os.path.join(self.pyfix_temp_folder, package_name)

        self.cur_lastfix = Lastfix(os.path.join(self.cur_package, 'XXXXXX_lastfix'),
                                   os.path.join(self.cur_package, 'XXXXXX_lastfix', 'lastfix_pyfix.csv'))
        print(f'\033[96m{package_name} - имя текущего пакета\033[0m')
        print()
        return package_name


class Workstation:
    def __init__(self, hostname, network_addresses, program_folder, client_folder, client_ver_file, lastfix_folder,
                 lastfix_file):
        self.hostname = hostname
        self.ip_address = None
        self.network_addresses = network_addresses

        self.net_path = f'\\\\{self.hostname}\\'
        self.program_folder = self.net_path + program_folder
        self.client_folder = self.net_path + client_folder
        self.client_ver_file = self.net_path + client_ver_file
        self.lastfix_folder = self.net_path + lastfix_folder
        self.lastfix_file = self.net_path + lastfix_file

        self.is_available = self._check_is_available()
        self.is_correct_network = self._check_if_correct_network()
        if self.is_correct_network:
            self.is_enough_privileges = self._check_is_enough_privileges()
            self.is_has_XXXXXX = self._check_is_has_XXXXXX()
            self.client = client(self.client_folder, self.client_ver_file, self.lastfix_folder, self.lastfix_file)
        else:
            self.is_enough_privileges = None
            self.is_has_XXXXXX = None
            self.client = None

        self.is_ready_to_fix = None
        self.is_fixed = None
        self.bad_user = None

    def _resolve_hostname(self):
        try:
            self.ip_address = socket.gethostbyname(self.hostname)
            return True
        except socket.gaierror:
            return False

    def _check_is_available(self):
        if not self._resolve_hostname():
            return False

        retries = 3
        while retries > 0:
            try:
                res = ping(self.ip_address, count=1)
            except RuntimeError:
                return False
            if res.stats_success_ratio > 0:
                return True
            else:
                retries -= 1
        else:
            return False

    def _check_if_correct_network(self):
        if self.ip_address:
            for network_address in self.network_addresses:
                if ipaddress.ip_address(self.ip_address) in ipaddress.ip_network(network_address):
                    return True
            else:
                return False
        else:
            return None

    def _check_is_enough_privileges(self):
        if self.is_available and self.is_correct_network:
            path = os.path.join(self.net_path, 'c$\\Windows')
            if os.path.exists(path):
                return True
            else:
                return False
        else:
            return None

    def _check_is_has_xxxxxx(self):
        if self.is_available and self.is_enough_privileges and os.path.exists(self.client_ver_file):
            return True
        else:
            return None

    def recheck_xxxxxx(self):
        print('\033[90m.\033[0m', end='')
        self.client = client(self.client_folder, self.client_ver_file, self.lastfix_folder, self.lastfix_file)
        print('\033[92m.\033[0m', end='')
