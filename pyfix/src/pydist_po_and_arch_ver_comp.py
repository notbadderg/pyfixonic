import os
import sys
import re
from .utilites import read_txt


def client_check(cfg):
    print('\033[96mПроверка наличия КЛИЕНТ ...\033[0m')
    condition = (os.path.exists(cfg.client_folder) and
                 os.path.exists(cfg.client_version_file) and
                 os.path.exists(cfg.client_folder + r'\Client\SOME_FILE.exe'))
    if condition:
        print('\033[92mКЛИЕНТ обнаружен.\033[0m')
        print()
        return
    else:
        sys.exit(f'\033[91mПо пути {cfg.client_folder} КЛИЕНТ не найден (или с ним проблемы), до свидания !\033[0m')


def ver_check(cfg):
    ver_pattern = r'\d+.\d+.\d+.\d+'

    print('\033[96mПроверка версий в именах архивов ...\033[0m')
    client_version = read_txt(cfg.client_version_file)
    print(f'Ищется такая строка в имени: {client_version} ...')
    condition = False
    if os.path.exists(cfg.archives_folder):
        raw_files = os.listdir(cfg.archives_folder)
        if raw_files:
            for file in raw_files:
                if file.split('.')[-1] not in ('rar', '7z', 'zip'):
                    print(f'\033[91mОбнаружен минимум один файл с посторонним расширением "{file}" !\033[0m')
                    break
                if client_version != re.search(ver_pattern, file).group(0):
                    print(f'\033[91mПроблема с версией КЛИЕНТ в минимум одном имени архива "{file}" !\033[0m')
                    break
            else:
                condition = True
        else:
            print(f'\033[91mПусто в {cfg.archives_folder} !\033[0m')
    else:
        print(f'\033[91mНе найден {cfg.archives_folder} !\033[0m')

    if condition:
        print('\033[92mАномалий нет.\033[0m')
        print()
        return
    else:
        sys.exit(f'\033[91mЭтап завершился неудачей, до свидания !\033[0m')


def client_and_arch_ver_comp(cfg):
    client_check(cfg)
    ver_check(cfg)
