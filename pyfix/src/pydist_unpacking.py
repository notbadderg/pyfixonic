import os
import sys
from .utilites import recreate_dir


def unpacking(archiver: str, src: str, dst: str) -> None:
    recreate_dir(dst)
    print('\033[96mТестирование архивов ...\033[0m')
    if os.system(archiver + ' t ' + src) != 0:
        sys.exit(f'\033[91mПроблема с одним из архивов !\033[0m')
    print('\033[92mТестирование архивов завершено.\033[0m')
    print()
    print('\033[96mРаспаковка архивов ...\033[0m')
    if os.system(archiver + ' x ' + src + ' ' + ' -o'+dst+'\\*') != 0:
        sys.exit(f'\033[91mПроблема с распаковкой одного из архивов !\033[0m')
    print('\033[92mРаспаковка архивов завершена.\033[0m')
    print()
