import os
import shutil
import sys
from .utilites import read_txt, create_lastfix, recreate_dir, create_fatal_failure_file, check_if_failure


def _check_if_failed_prev_backup_or_restore(cfg):
    if os.path.exists(cfg.backup_flag):
        create_fatal_failure_file(cfg)
        print(f'\033[91Создание предыдущего бекапа не завершилось подобающим образом !\033[0m')
        print()
        check_if_failure(cfg)

    if os.path.exists(cfg.restore_flag):
        create_fatal_failure_file(cfg)
        print(f'\033[91Прошлое восстановление не завершилось подобающим образом !\033[0m')
        print()
        check_if_failure(cfg)


def backup(cfg):
    print('\033[96mНачало создания бекапа ...\033[0m')

    _check_if_failed_prev_backup_or_restore(cfg)

    with open(cfg.backup_flag, 'w') as f:
        f.write('uwu')

    if os.path.exists(cfg.client_folder):
        if os.path.exists(cfg.client_backup):
            print(f'Обнаружен и будет удален: {cfg.client_backup} ... ')
            shutil.rmtree(cfg.client_backup)
        print(f'Создается резервная копия {cfg.client_folder} в {cfg.client_backup} ...')
        shutil.copytree(cfg.client_folder, cfg.client_backup)
    else:
        sys.exit(f'\033[91mНе найден путь {cfg.client_folder} !\033[0m')

    if os.path.exists(cfg.lastfix_folder):
        if os.path.exists(cfg.lastfix_backup):
            print(f'Обнаружен и будет удален: {cfg.lastfix_backup} ... ')
            shutil.rmtree(cfg.lastfix_backup)
        print(f'Создается резервная копия {cfg.lastfix_folder} в {cfg.lastfix_backup} ...')
        shutil.copytree(cfg.lastfix_folder, cfg.lastfix_backup)
    else:
        print(f'Не  обнаружен текущий {cfg.lastfix_folder}, '
              f'для бекапа будет создан {cfg.lastfix_backup} с lastfix по умолчанию ...')

        recreate_dir(cfg.lastfix_backup)
        create_lastfix(os.path.join(cfg.lastfix_backup, cfg.lastfix_file.split('\\')[-1]),
                       read_txt(cfg.client_version_file),
                       0.0)
    print('\033[92mБекап создан.\033[0m')
    os.remove(cfg.backup_flag)
    print()


def restore(cfg, do_exit=True):
    print('\033[96mНачало восстановления из бекапа ...\033[0m')

    _check_if_failed_prev_backup_or_restore(cfg)

    with open(cfg.restore_flag, 'w') as f:
        f.write('uwu')

    if os.path.exists(cfg.lastfix_folder):
        shutil.rmtree(cfg.lastfix_folder)
    if not os.path.exists(cfg.client_backup):
        create_fatal_failure_file(cfg)
        sys.exit(f'\033[91mНе найден {cfg.client_backup} - не из чего восстанавливать !\033[0m')
    shutil.rmtree(cfg.client_folder)
    # os.rename(cfg.client_backup, cfg.client_folder)
    # os.rename(cfg.lastfix_backup, cfg.lastfix_folder)
    shutil.copytree(cfg.client_backup, cfg.client_folder, dirs_exist_ok=True)
    shutil.copytree(cfg.lastfix_backup, cfg.lastfix_folder, dirs_exist_ok=True)
    if os.path.exists(cfg.lastfix_folder) and os.path.exists(cfg.client_folder):
        print('\033[92mЗавершено восстановление из бекапа.\033[0m')
        os.remove(cfg.restore_flag)
        print()
        if os.path.exists(cfg.indexation_flag):
            os.remove(cfg.indexation_flag)
        if do_exit:
            sys.exit('\033[91mУстановка завершилась неудачно, но дистрибутив восстановлен.\033[0m')
        else:
            return
    else:
        create_fatal_failure_file(cfg)
        sys.exit('\033[91mЧто-то пошло не так (не обнаружен один из каталогов, или оба) !\033[0m')
