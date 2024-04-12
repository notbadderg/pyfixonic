import os
import sys
from .utilites import read_txt, read_lastfix
from .pydist_backup import restore
import time


def fix_logic(cfg, sorted_fixes: list) -> list:
    print('\033[96mНачало принятия решения ...\033[0m')

    if os.path.exists(cfg.indexation_flag):
        print(f'\033[91mОбнаружен признак того, что прошлый запуск PYDIST был досрочно прерван '
              f'(до завершения индексации) !\033[0m')
        print(f'\033[91mТребуется откат к последнему бекапу !\033[0m')
        print()
        restore(cfg, do_exit=False)

    client_version = read_txt(cfg.client_version_file)

    current_fix = 0.0
    if not os.path.exists(cfg.lastfix_file):
        print('\033[93mНе обнаружен lastfix_pyfix.csv, '
              'будет считаться, что на дистрибутиве фиксы еще не установлены.\033[0m')
    else:
        lastfix_content = read_lastfix(cfg.lastfix_file)
        print(f'\033[95mСодержимое {cfg.lastfix_file}:\033[0m')
        print('\tVersion:\t', end='')
        print(f'\033[92m{lastfix_content["Version"]}\033[0m')
        print('\tFix:\t\t', end='')
        print(f'\033[92m{lastfix_content["Fix"]}\033[0m')
        print()

        if lastfix_content['Version'] == client_version:
            current_fix = lastfix_content['Fix']
            print('\033[92mВерсия совпадает.\033[0m')
        else:
            print('\033[93mВерсия в lastfix_pyfix.csv не соответствует, '
                  'будет считаться, что на дистрибутиве фиксы еще не установлены.\033[0m')
            current_fix = 0.0

    max_fix = max(sorted_fixes)[0]
    print(f'Последний номер фикса в папке с архивами: {max_fix}')
    if current_fix > max_fix:
        time.sleep(0.5)
        sys.exit(f'\033[91mУстановлен уже более новый фикс ({current_fix}), '
                 f'чем есть в каталоге для распространения ({max_fix}) !\033[0m')
    elif current_fix == max_fix:
        time.sleep(0.5)
        sys.exit(f'\033[91mПоследний фикс {current_fix} уже установлен !\033[0m')

    fixes_to_install = []
    previous_fix = float()
    gap_check = True
    for fix in sorted_fixes:
        if round(fix[0] % 1 * 10 % 1, 3) != 0:
            sys.exit(f'\033[91mРабота с сотыми долями не поддерживается ({fix[0]}) !\033[0m')
        if fix[0] <= current_fix:
            continue
        if gap_check and fix[0] > current_fix:
            previous_fix = current_fix
            gap_check = False
        condition_1 = (fix[0] % 1 == 0) and (previous_fix % 1 == 0) and round(fix[0] - previous_fix, 3) == 1
        condition_2 = (fix[0] % 1 == 0) and (previous_fix % 1 != 0) and round(fix[0] - previous_fix, 3) < 1
        condition_3 = ((fix[0] % 1 != 0) or (previous_fix % 1 != 0)) and round(fix[0] - previous_fix, 3) == 0.1
        if condition_1 or condition_2 or condition_3:
            fixes_to_install.append(fix)
            previous_fix = fix[0]
        else:
            time.sleep(0.5)
            sys.exit(f'\033[91mОбнаружен промежуток между версиями: {previous_fix} >>> ??? >>> {fix[0]}\033[0m')

    print('\033[92mРазрывы в нумерации не обнаружены.\033[0m')
    print(f'\033[93mРЕШЕНИЕ\033[0m - Будут установлены фиксы:')
    [print('\033[95m\t', fix[0], '\033[0m') for fix in fixes_to_install]
    print('')
    print('\033[92mКонец принятия решения.\033[0m')
    print()
    return fixes_to_install
