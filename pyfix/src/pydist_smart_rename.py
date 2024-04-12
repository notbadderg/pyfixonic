import os
import sys
import shutil
import time
import math
import re
from .utilites import recreate_dir


def smart_rename(archives_folder: str, renaming_folder: str) -> None:
    print('\033[96mНачало переименования ...\033[0m')
    pattern = r'(\d+.\d+.\d+.\d)(\D*)(\d+[.]?\d?)'
    recreate_dir(renaming_folder)
    raw_archives = []
    for file in os.listdir(archives_folder):
        raw_archives.append(file)

    archives = {}
    for archive in raw_archives:
        temp_name = os.path.splitext(archive)[0]
        fix_version = re.search(pattern, temp_name).group(3)
        try:
            archives[archive] = float(fix_version)
        except ValueError:
            sys.exit(f'\033[91mЧто-то не так с именем у {archive} !\033[0m')

    # check for continuous of fixes:
    set_fix_numbers = set()
    for k, v in archives.items():
        if v.is_integer() != 0:
            set_fix_numbers.add(k)
    if 0 in archives.values():
        sys.exit(f'\033[91mВ {archives_folder} есть фикс с номером ноль, серьезно?\033[0m')

    if math.floor(max(archives.values())) != len(set_fix_numbers):
        sys.exit(f'\033[91mВ {archives_folder} не сходится номер последнего фикса и их количество '
                 f'(дробные фиксы не считаются). Какой-то пропущен или есть лишний?\033[0m')

    archives = sorted(archives.items(), key=lambda item: item[1])
    for k, v in archives:
        new_filename = str(v)+os.path.splitext(k)[1]
        new_path = os.path.join(renaming_folder, new_filename)
        print(f'{k}\t--->\t{new_filename}')
        shutil.copy(os.path.join(archives_folder, k), new_path)

    print('\033[92mКонец переименования.\033[0m')
    print()
    print("\033[93m! ВНИМАНИЕ !")
    print('  ПРОВЕРЬТЕ визуально, что переименование прошло верно!')
    print('\033[0m')
    print('(При обнаружении ошибки - прервите работу программы. Выполнение сейчас продолжится.)')
    secs = 5
    while secs > 0:
        secs -= 1
        print(secs, end='')
        time.sleep(1)
    print()
    print()
