import os
import sys
from src.pydist_backup import backup, restore
from src.utilites import create_lastfix, read_lastfix, read_txt, recreate_dir
import shutil


def fix_install(cfg, fixes_to_install: list):
    backup(cfg)
    print('\033[96mНачало установки фиксов ...\033[0m')

    with open(cfg.indexation_flag, 'w') as f:
        f.write('uwu')

    last_fix = 0.0
    for fix in fixes_to_install:
        print(f'\033[95mУстановка фикса {fix[0]} ...\033[0m')
        src = fix[1]
        dst = cfg.client_folder
        shutil.copytree(src, dst, dirs_exist_ok=True)
        res = os.system(r'"C:\Program Files (x86)\XXXXXX\Client\SOME_FILE_2.exe"')
        if res != 0:
            print(f'\033[91mУстановка фикса {fix[0]} неудачна ! \033[0m')
            restore(cfg)
        else:
            print(f'\033[92mУстановка фикса {fix[0]} выполнена.\033[0m')
            print()
            last_fix = fix[0]
    recreate_dir(cfg.lastfix_folder)
    create_lastfix(cfg.lastfix_file, read_txt(cfg.client_version_file), last_fix)
    print()
    if os.path.exists(cfg.lastfix_file):
        new_lastfix = read_lastfix(cfg.lastfix_file)
        print(f'\033[95mСодержимое нового {cfg.lastfix_file}:\033[0m')
        print('\tVersion:\t', end='')
        print(f'\033[92m{new_lastfix["Version"]}\033[0m')
        print('\tFix:\t\t', end='')
        print(f'\033[92m{new_lastfix["Fix"]}\033[0m')
        print('\033[92mУстановка фиксов завершена!\033[0m')
        print()
        os.remove(cfg.indexation_flag)
    else:
        sys.exit(f'\033[91mНе найден {cfg.lastfix_file} !\033[0m')
