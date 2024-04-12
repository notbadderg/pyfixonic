import os
from .utilites import recreate_dir


def write_results(cfg, package_name, wss):
    def _write(path, list_):
        with open(path, 'w') as f:
            for e in list_:
                f.write(e + '\n')

    res_folder = os.path.join(cfg.serv_result_folder, package_name)
    recreate_dir(res_folder)
    good_res_file = os.path.join(res_folder, cfg.serv_result_good)
    not_available_res_file = os.path.join(res_folder, cfg.serv_result_not_available)
    error_res_file = os.path.join(res_folder, cfg.serv_result_error)
    error_res_with_codes_file = os.path.join(res_folder, cfg.serv_result_error_with_codes)
    good_list = []
    not_available_list = []
    error_list = []
    error_list_with_codes = []
    for ws in wss.values():
        if ws.is_correct_network is True:
            if isinstance(ws.is_fixed, str) and 'ERR' in ws.is_fixed:
                error_list.append(ws.hostname)
                error_list_with_codes.append(f'{ws.hostname}---{ws.is_fixed[3:]}')
            elif ws.is_fixed is True:
                good_list.append(ws.hostname)
            else:
                not_available_list.append(ws.hostname)
        else:
            not_available_list.append(ws.hostname)
    _write(good_res_file, good_list)
    _write(not_available_res_file, not_available_list)
    _write(error_res_file, error_list)
    _write(error_res_with_codes_file, error_list_with_codes)
