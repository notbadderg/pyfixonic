from src.pydist_smart_rename import smart_rename
from src.pydist_unpacking import unpacking
from src.utilites import get_fixes_list, check_if_failure, warning, wait_podumay
from src.pydist_make_cumulative import make_cumulative
from src.pydist_fix_logic import fix_logic
from src.pydist_fix_install import fix_install
from src.colorama import just_fix_windows_console
from src.pydist_po_and_arch_ver_comp import client_and_arch_ver_comp
import time


class Config:
    def __init__(self):
        self.disk = r'c:'

        self.pyfixonic_path = self.disk + '\\!pyfixonic'
        self.archives_folder = self.pyfixonic_path + '\\fixes'
        self.renaming_folder = self.pyfixonic_path + '\\pyfix\\temp\\renaming'
        self.unpacked_folder = self.pyfixonic_path + '\\pyfix\\temp\\unpacked'
        self.cumulative_folder = self.pyfixonic_path + '\\pyfix\\temp\\cumulative'
        self.cumulative_lastfix_file = self.pyfixonic_path + '\\pyfix\\temp\\cumulative\\lastfix_pyfix.csv'

        self.backup_flag = self.pyfixonic_path + '\\pyfix\\temp\\backup_in_progress.flag'
        self.restore_flag = self.pyfixonic_path + '\\pyfix\\temp\\restore_in_progress.flag'
        self.indexation_flag = self.pyfixonic_path + '\\pyfix\\temp\\indexation_in_progress.flag'

        self.fatal_failure_flag = self.pyfixonic_path + '\\pyfix\\temp\\fatal_failure.flag'

        self.archiver = r'"C:\Program Files\7-Zip\7z.exe"'
        self.client_folder = self.disk + r'\Program Files (x86)\XXXXXX'
        self.client_version_file = self.client_folder + r'\Client\version.txt'
        self.lastfix_folder = self.disk + r'\Program Files (x86)\XXXXXX_lastfix'
        self.lastfix_file = self.lastfix_folder + r'\lastfix_pyfix.csv'

        self.client_backup = self.client_folder + r'_back_pyfix'
        self.lastfix_backup = self.lastfix_folder + r'_back_pyfix'


def pydist_auto():
    warning()
    wait_podumay(20)
    print('\033[96mНачало выполнения ...\033[0m')
    print()
    cfg = Config()

    check_if_failure(cfg)

    client_and_arch_ver_comp(cfg)
    time.sleep(0.5)
    smart_rename(cfg.archives_folder, cfg.renaming_folder)
    time.sleep(0.5)
    unpacking(cfg.archiver, cfg.renaming_folder, cfg.unpacked_folder)
    time.sleep(0.5)
    sorted_fixes = get_fixes_list(cfg.unpacked_folder)
    time.sleep(0.5)
    fixes_to_install = fix_logic(cfg, sorted_fixes)
    time.sleep(0.5)
    fix_install(cfg, fixes_to_install)
    time.sleep(0.5)
    make_cumulative(sorted_fixes, cfg)
    time.sleep(0.5)
    print()
    print('\033[92mВыполнение завершено.\033[0m')


if __name__ == '__main__':
    just_fix_windows_console()
    pydist_auto()
