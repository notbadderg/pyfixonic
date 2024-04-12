import os.path
import shutil
import subprocess
import time

from src.pyfix_class_server_ws import Workstation
from src.utilites import timer, find_all_exe, ParallelPrint
import concurrent.futures as cf


def _print_legend():
    print(f'\033[96mЗапуск фиксования ... \033[0m')
    print('СТАТУСНЫЕ КОДЫ (в скобках):')
    print('\t0 - не имеет признака готовности к фиксованию')
    print('\t1 - неудачный прошлый запуск, разберитесь вручную и удалите флаг')
    print('\t2 - не удалось завершить один из .exe процессов в папке XXXXXX')
    print('\t3 - не удалось удалить файл запуска КЛИЕНТ')
    print('\t4 - (зарезервирован, не реализован)')
    print('\t5 - не удалось переименовать файл запуска КЛИЕНТ')
    print('\t6 - не удалось удалить флаг фиксования')
    print('\t7 - ошибок нет')
    print()
    print('\t! - признак нехорошего человека (не выключен КЛИЕНТ)')
    print()


def _print_legend_check_flag():
    print(f'\033[96mЗапуск проверки флага фиксования... \033[0m')
    print('СТАТУСНЫЕ КОДЫ (в скобках):')
    print('\t0  - не имеет признака готовности')
    print('\t1  - обнаружен флаг фиксования')
    print('\t9 - не обнаружен флаг фиксования')
    print()


def _fixing_flag_check(ws, fixing_flag):
    if os.path.exists(fixing_flag):
        ws.is_ready_to_fix = False
        return True
    else:
        return False


def _fixing_flag_set(ws, fixing_flag):
    if not os.path.exists(ws.client.lastfix.folder):
        os.mkdir(ws.client.lastfix.folder)
    with open(fixing_flag, 'w') as f:
        f.write('uwu')


def _fixing_flag_remove(fixing_flag):
    try:
        os.remove(fixing_flag)
    except FileNotFoundError or PermissionError or Exception:
        return False
    else:
        return True


def _kill_client_process(ws):
    def _get_pid(host, process_name):

        # command = f'tasklist /S {host} /FI "IMAGENAME eq {process_name}" /FO CSV /NH'
        # subprocess.getoutput('chcp 866')

        process_name_without_exe = process_name[:-4]
        command = f'pyfix\\src\\pslist.exe -nobanner \\\\{host} "{process_name_without_exe}"'

        out = subprocess.getoutput(command)

        # list_ = out.split('","')
        # if len(list_) > 1:
        #     return int(list_[1].strip())
        # else:
        #     return None
        if 'Elapsed Time' in out:
            return process_name
        else:
            return None

    def _kill_pid(host, process):
        # command = f'pyfix\\src\\psexec.exe \\\\{host} cmd /c "taskkill /f /PID {process}"'

        command = f'pyfix\\src\\psexec.exe \\\\{host} cmd /c "taskkill /f /IM {process}"'

        return subprocess.getoutput(command)

    def _killing_loop(ws_, execs_):
        for exe_ in execs_:
            if _get_pid(ws.hostname, exe_):
                ws_.bad_user = True
                retries = 15
                while retries > 0:
                    pid = _get_pid(ws.hostname, exe_)
                    out = _kill_pid(ws.hostname, pid)
                    if '0.' not in out:
                        # print(f'! {ws.hostname} psexec/taskkill output: {out}')
                        pass
                    if not _get_pid(ws.hostname, exe_):
                        break
                    retries -= 1
                    time.sleep(2)
                else:
                    return False
        return True

    execs = find_all_exe(ws.client.folder)
    # Repeating 2 times to ensure.
    _killing_loop(ws, execs)
    if _killing_loop(ws, execs):
        return True
    else:
        return False


def _delete_client_exe(ws):
    path = os.path.join(ws.client.folder, 'SOME_FILE.exe')
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            return False
        return True
    else:
        return False


def _rename_client_exe_wait(ws):
    old = os.path.join(ws.client.folder, 'SOME_FILE.exe.wait')
    new = os.path.join(ws.client.folder, 'SOME_FILE.exe')
    if os.path.exists(old):
        os.rename(old, new)
        return True
    else:
        return False


def _copy_package(server, ws):
    src_ = server.cur_package
    dst_ = ws.program_folder
    shutil.copytree(src_, dst_, dirs_exist_ok=True)


def _fixing(server, ws, is_ignore_fixing_flag, is_only_check_fixing_flag, pp):
    def _print_color_number(color, n_, e_):
        if color == 'green':
            c = '\033[92m'
        elif color == 'red':
            c = '\033[91m'
        elif color == 'gray':
            c = '\033[90m'
        elif color == 'yellow':
            c = '\033[93m'
        else:
            c = ''
        pp.p(f'{c} {n_}({e_}{c})\t\033[0m')

    def _set_error(ws_, n, e):
        ws_.is_fixed = f'ERR{e}'
        _print_color_number('red', n, e)
        return False

    pp.p(f'\033[90m({ws.hostname})\t\033[0m')

    if not ws.is_ready_to_fix or not ws.is_correct_network:
        return _print_color_number('gray', ws.hostname, 0)

    time.sleep(0.5)
    fixing_flag = os.path.join(ws.client.lastfix.folder, 'fixing.flag')
    if not is_ignore_fixing_flag and _fixing_flag_check(ws, fixing_flag):
        return _set_error(ws, ws.hostname, 1)

    if is_only_check_fixing_flag:
        return _print_color_number('yellow', ws.hostname, 9)

    _fixing_flag_set(ws, fixing_flag)

    time.sleep(0.5)
    if not _kill_client_process(ws):
        return _set_error(ws, ws.hostname, 2)

    time.sleep(0.5)
    if not _delete_client_exe(ws):
        return _set_error(ws, ws.hostname, 3)

    time.sleep(0.5)
    _copy_package(server, ws)

    time.sleep(0.5)
    if not _rename_client_exe_wait(ws):
        return _set_error(ws, ws.hostname, 5)

    time.sleep(0.5)
    if not _fixing_flag_remove(fixing_flag):
        return _set_error(ws, ws.hostname, 6)

    time.sleep(0.5)
    if ws.bad_user:
        fool_detector = '\033[33m!'
    else:
        fool_detector = ''

    time.sleep(0.1)
    return _print_color_number('green', ws.hostname, '7'+fool_detector)


class Fixer:
    def __init__(self, ws, server, is_ignore_fixing_flag, is_only_check_fixing_flag, pp):
        self.ws = ws
        self.server = server
        self.is_ignore_fixing_flag = is_ignore_fixing_flag
        self.is_only_check_fixing_flag = is_only_check_fixing_flag
        self.pp = pp

    def fix(self):
        try:
            _fixing(self.server, self.ws, self.is_ignore_fixing_flag, self.is_only_check_fixing_flag, self.pp)
        except Exception as ex:
            print(f'\033[91m{self.ws.hostname} - {ex}\033[0m')
            print()


@timer
def fixing_threader(server, wss: dict, is_ignore_fixing_flag, is_only_check_fixing_flag, max_workers=30) -> dict:
    if is_only_check_fixing_flag:
        if is_ignore_fixing_flag:
            print('\033[91m! Будет проигнорирован признак игнорирования флага, '
                  'потому что запущен режим только проверки флагов.\033[0m')
            print()
            is_ignore_fixing_flag = False
        _print_legend_check_flag()
    else:
        _print_legend()
    print('\033[93mВыполнение:\033[0m \033[90m[имя_компьютера]([статус])\033[0m')
    print(f'\033[90mВ скобках - запуск задачи на компьютере, без скобок - задача завершена.\033[0m')
    print()

    list_ = []
    p_print_2 = ParallelPrint()
    for ws in wss.values():
        if ws.is_correct_network:
            list_.append(Fixer(ws, server, is_ignore_fixing_flag, is_only_check_fixing_flag, p_print_2))
    pool = cf.ThreadPoolExecutor(max_workers=max_workers)
    for e in list_:
        pool.submit(Fixer.fix, e)
        time.sleep(0.1)
    pool.shutdown(wait=True)
    print()
    print()
    return wss
