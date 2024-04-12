from src.pyfix_startup import *
from src.pyfix_preparations import make_server, get_hostnames, make_wss, check_fix_status, rechecking
from src.pyfix_write_results import write_results
from src.pyfix_print_results import print_res, count_res
from src.utilites import timer, wait_podumay, deco_print_long_lines, warning
from src.colorama import just_fix_windows_console
from src.pyfix_fixing import fixing_threader


class Config:
    def __init__(self):
        self.serv_cumulative_folder = r'C:\!pyfixonic\pyfix\temp\cumulative\Client'
        self.serv_cumulative_lastfix_file = r'C:\!pyfixonic\pyfix\temp\cumulative\lastfix_pyfix.csv'
        self.serv_ws_list_file = r'C:\!pyfixonic\input\ws_all.txt'
        self.serv_test_ws_list_file = r'C:\!pyfixonic\input\ws_all_test.txt'
        self.serv_result_folder = r'C:\!pyfixonic\result'
        self.serv_result_good = 'good.txt'
        self.serv_result_not_available = 'not_available.txt'
        self.serv_result_error = 'error.txt'
        self.serv_result_error_with_codes = 'error_with_codes.txt'
        self.serv_pyfix_temp_folder = r'C:\!pyfixonic\pyfix\temp\pyfix'

        self.ws_program_folder = r'\c$\Program Files (x86)'
        self.ws_client_folder = r'XXXXX'
        self.ws_client_ver_file = r'XXXXX\version.txt'
        self.ws_lastfix_folder = r'XXXXX_lastfix'
        self.ws_lastfix_file = r'XXXXX_lastfix\lastfix_pyfix.csv'


@timer
def pyfix_auto():
    warning()
    wait_podumay(20)

    print()
    is_ignore = get_is_ignore_fixing_flag()
    is_only_check_flag = get_is_only_check_fixing_flag()

    cfg = Config()
    server = make_server(cfg)
    package_name = server.prepare_package()

    hostnames = get_hostnames(cfg, get_is_testing())
    wss = make_wss(cfg, hostnames, get_networks())
    wss = check_fix_status(server, wss)

    print_res(wss)
    wait_podumay(12)

    wss = fixing_threader(server, wss, is_ignore, is_only_check_flag)

    if not is_only_check_flag:
        deco_print_long_lines()
        wss = rechecking(wss)
        wss = check_fix_status(server, wss)
        print_res(wss)
        count_res(wss)
        write_results(cfg, package_name, wss)


if __name__ == '__main__':
    just_fix_windows_console()
    pyfix_auto()
