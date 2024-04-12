import concurrent.futures as cf
from time import perf_counter, sleep
import os
import shutil
import csv
import sys
import time
from datetime import datetime


def timer(func):
    def wrapper(*args, **kwargs):
        t_start = perf_counter()
        result = func(*args, **kwargs)
        t_stop = perf_counter()
        print(f'\033[95mВыполнение {func.__name__} заняло (сек): {round(t_stop-t_start, 2)}\033[0m')
        print()
        return result
    return wrapper


def threader(iter_, func, max_=999, **kwargs):
    pool = cf.ThreadPoolExecutor(max_workers=max_)
    for item in iter_:
        print(f'Processing {item.hostname} ...')
        pool.submit(func, item, **kwargs)
    pool.shutdown(wait=True)


def recreate_dir(path: str, create=True) -> None:
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        if create:
            os.mkdir(path)
    except PermissionError:
        sys.exit('\033[91mОтказано в доступе!\033[0m')


def get_fixes_list(dst: str) -> list:
    path = os.path.join(dst)
    folders = os.listdir(path)
    list_ = []
    for folder in folders:
        list_.append((float(folder), os.path.join(path, folder)))
    list_.sort()
    return list_


def read_txt(path):
    with open(path, 'r') as f:
        return f.readline()


def create_lastfix(file: str, ver: str, fix: float) -> None:
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        header = ['Version', 'Fix']
        row = [ver, fix]
        writer.writerows([header, row])


def read_lastfix(path: str) -> dict:
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        # headers into void
        next(reader)
        row = next(reader)
        dict_ = {
            'Version': row[0].strip(),
            'Fix': float(row[1].strip())
        }
    return dict_


def check_if_failure(cfg):
    if os.path.exists(cfg.fatal_failure_flag):
        print('\033[91m ! Обнаружен признак неисправности дистрибутива КЛИЕНТ:\033[0m')
        print('- переустановите клиент (не надо, если есть папка с нулёвым КЛИЕНТ), вручную удалите папки (если есть):')
        print('\t', cfg.client_folder)
        print('\t', cfg.client_backup)
        print('\t', cfg.lastfix_folder)
        print('\t', cfg.lastfix_backup)
        print()
        print('- инсталлируйте чистый КЛИЕНТ (или возьмите из папки с нулёвым КЛИЕНТ, если есть) '
              'и \033[91m только после\033[0m этого удалите вручную этот файл:')
        print('\t', cfg.fatal_failure_flag)
        print()
        print('- потом попытайтесь ещё раз установить фиксы.')
        print()
        sleep(2)
        sys.exit('\033[91mУвы.\033[0m')


def create_fatal_failure_file(cfg):
    with open(cfg.fatal_failure_flag, 'w') as f:
        f.write('salam aleikum')


def get_date_for_folder_name() -> str:
    n = datetime.now().timetuple()
    return f'{n[0]}-{n[1]}-{n[2]}_{n[3]}-{n[4]}-{n[5]}'


def find_all_exe(path: str) -> list:
    exe_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.exe':
                exe_files.append(file)
    return exe_files


def wait_podumay(sec: float) -> None:
    print(f'\033[93mОжидание {sec} секунд - закройте программу, если передумали или что-то не так.\033[0m')
    print()
    sleep(sec)


def deco_print_long_lines() -> None:
    print()
    print('='*101)
    print('='*101)
    print()
    print()


def deco_print_n_elements_in_row(list_, max_count=5) -> None:
    print('\033[96mСодержимое списка:\033[0m')
    cur_count = 0
    for e in list_:
        if cur_count == max_count:
            print()
            cur_count = 0
        print(f'{e}\t', end='')
        cur_count += 1
    else:
        print()
        print()


class ParallelPrint:
    def __init__(self, wide=4):
        self.wide = wide
        self.in_current_row_count = 0

    def p(self, string: str) -> None:
        if self.in_current_row_count == self.wide:
            print()
            self.in_current_row_count = 0
        print(f'{string}\t', end='')
        self.in_current_row_count += 1


def warning():
    print()
    print('\033[91mВНИМАНИЕ\033[0m')
    print()
    print('Программа разработана исключительно как инструмент для личного пользования, позволяющего повысить скорость\n'
          'выполнения задач, которые решаются данной программой.')
    print()
    print('Продолжая, Вы подтверждаете и соглашаетесь с тем, что:\n'
          '- автор \033[91mне несёт никакой ответственности\033[0m за любой результат выполнения этой '
          'программы;\n'
          '- автор \033[91mне оказывает никакую техническую поддержку\033[0m на любом этапе использования этой '
          'программы;\n'
          '- пользователь программы (запускающий эту программу) обладает всеми необходимыми явными и неявными\n'
          '  полномочиями на действия, которые это программа совершает;\n'
          '- пользователь программы (запускающий эту программу) обладает необходимой квалификацией и знаниями для\n'
          '  самостоятельного решения возникающих проблем на любом этапе использования этой программы, включая, но\n'
          '  не ограничиваясь: знание Python 3, основ системного и сетевого администрирования, пакета PsTools.')

    print()
