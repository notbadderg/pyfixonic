import time
import concurrent.futures as cf
from src.pyfix_class_server_ws import Server, Workstation
from src.utilites import timer, deco_print_n_elements_in_row, ParallelPrint


def get_hostnames(cfg, dist_testing=True):
    if dist_testing:
        path = cfg.serv_test_ws_list_file
    else:
        path = cfg.serv_ws_list_file

    hostnames = set()
    with open(path, 'r') as f:
        list_ = f.readlines()
        for line in list_:
            temp_line = line.strip().lower()
            if not temp_line:
                continue
            if temp_line[0] == '#':
                continue
            elif temp_line == '-----':
                break
            elif temp_line[0] != '-':
                hostnames.add(temp_line)
    return sorted(list(hostnames))


def make_server(cfg) -> Server:
    return Server(cumulative_folder=cfg.serv_cumulative_folder,
                  cumulative_lastfix_file=cfg.serv_cumulative_lastfix_file,
                  ws_list_file=cfg.serv_ws_list_file,
                  test_ws_list_file=cfg.serv_test_ws_list_file,
                  pyfix_temp_folder=cfg.serv_pyfix_temp_folder)


def _create_ws(cfg, dict_, hostname, networks, pp):
    pp.p(f'\033[90m({hostname})\033[0m')
    dict_[hostname] = Workstation(hostname=hostname,
                                  network_addresses=networks,
                                  program_folder=cfg.ws_program_folder,
                                  client_folder=cfg.ws_client_folder,
                                  client_ver_file=cfg.ws_client_ver_file,
                                  lastfix_folder=cfg.ws_lastfix_folder,
                                  lastfix_file=cfg.ws_lastfix_file)
    time.sleep(0.05)
    pp.p(f' {hostname} ')


@timer
def make_wss(cfg, hostnames: list, networks: list, max_workers=60, print_list=True) -> dict:
    pool = cf.ThreadPoolExecutor(max_workers=max_workers)
    dict_ = {}
    if print_list:
        deco_print_n_elements_in_row(hostnames)

    print(f'\033[96mПолучение статуса:\033[0m \033[90m[имя_компьютера]\033[0m')
    print(f'\033[90mВ скобках - запуск задачи на компьютере, без скобок - задача завершена.\033[0m')
    print()
    p_print = ParallelPrint()
    for hostname in hostnames:
        pool.submit(_create_ws, cfg=cfg, dict_=dict_, hostname=hostname, networks=networks, pp=p_print)
        time.sleep(0.05)
    pool.shutdown(wait=True)
    print()
    return dict_


@timer
def rechecking(wss: dict, max_workers=60) -> dict:
    print('\033[93mПерепроверка КЛИЕНТ на компьютерах, подождите \033[0m', end='')
    pool = cf.ThreadPoolExecutor(max_workers=max_workers)
    for ws in wss.values():
        if ws.is_correct_network:
            pool.submit(Workstation.recheck_client, ws)
            time.sleep(0.05)
    pool.shutdown(wait=True)
    print()
    return wss


def check_fix_status(s: Server, wss: dict) -> dict:
    for ws in wss.values():
        if isinstance(ws.is_fixed, str) and 'ERR' in ws.is_fixed:
            ws.is_ready_to_fix = False
            continue

        if not ws.is_available:
            ws.is_ready_to_fix = False
            ws.is_fixed = None

        elif ws.is_available and ws.is_correct_network:
            if not ws.is_enough_privileges:
                ws.is_ready_to_fix = False
                ws.is_fixed = None

            elif (not ws.is_has_client or
                    ws.client.ver != s.cur_lastfix.ver):
                ws.is_ready_to_fix = False
                ws.is_fixed = False

            elif (ws.client.ver == ws.client.lastfix.ver == s.cur_lastfix.ver and
                    ws.client.lastfix.fix == s.cur_lastfix.fix):
                ws.is_ready_to_fix = False
                ws.is_fixed = True

            elif (ws.client.ver == s.cur_lastfix.ver and
                  ws.client.ver != ws.client.lastfix.ver or
                  ws.client.ver == ws.client.lastfix.ver == s.cur_lastfix.ver and
                  ws.client.lastfix.fix < s.cur_lastfix.fix):
                ws.is_ready_to_fix = True
                ws.is_fixed = False

        else:
            ws.is_ready_to_fix = False
            ws.is_fixed = None
    return wss
