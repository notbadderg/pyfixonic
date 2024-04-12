import os


def get_networks() -> list:
    pyfix_networks_raw_list = os.getenv('PYFIX_TARGET_NETWORKS').split(',')
    pyfix_networks = []
    for e in pyfix_networks_raw_list:
        temp_e = e.strip().lower()
        pyfix_networks.append(temp_e)
    return pyfix_networks


def get_is_testing() -> bool:
    if os.getenv('PYFIX_TESTING') == '0':
        is_testing = False
        print(f'\033[93mРЕЖИМ ТЕСТИРОВАНИЯ СБОРКИ \033[91mОТКЛЮЧЕН\033[0m')
    else:
        is_testing = True
        print(f'\033[93mРЕЖИМ ТЕСТИРОВАНИЯ СБОРКИ\033[0m')
    print()
    return is_testing


def get_is_ignore_fixing_flag() -> bool:
    if os.getenv('PYFIX_IGNORE_FIXING_FLAG') == '1':
        is_ignore_fixing_flag = True
        print(f'\033[93mВКЛЮЧЕНО ИГНОРИРОВАНИЕ ФЛАГА НЕУДАЧНОЙ УСТАНОВКИ \033[91m\033[0m')
        print()
    else:
        is_ignore_fixing_flag = False
    return is_ignore_fixing_flag


def get_is_only_check_fixing_flag() -> bool:
    if os.getenv('PYFIX_ONLY_CHECK_FIXING_FLAG') == '1':
        is_only_check_fixing_flag = True
        print(f'\033[93mВКЛЮЧЕН РЕЖИМ ПРОВЕРКИ ТОЛЬКО НАЛИЧИЯ ФЛАГА (без установки фиксов) \033[91m\033[0m')
        print()
    else:
        is_only_check_fixing_flag = False
    return is_only_check_fixing_flag
