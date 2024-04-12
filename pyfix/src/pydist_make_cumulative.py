import shutil
import os
from .utilites import recreate_dir


def _finish_prepare_cumulative(cfg):
    shutil.copy(cfg.lastfix_file, cfg.cumulative_lastfix_file)
    files_to_grab = ['Client\\AssemblyCache.dat',
                     'Client\\CatalogIndex\\index.xml',
                     'Client\\CatalogIndex\\index.pgmdb',
                     'Client\\SOME_FILE.exe']

    os.mkdir(os.path.join(cfg.cumulative_folder, 'Client\\CatalogIndex'))
    for file in files_to_grab:
        src = os.path.join(cfg.client_folder, file)
        dst = os.path.join(cfg.cumulative_folder, file)
        shutil.copy(src, dst)

    old = os.path.join(cfg.cumulative_folder, 'Client\\SOME_FILE.exe')
    new = os.path.join(cfg.cumulative_folder, 'Client\\SOME_FILE.exe.wait')
    os.rename(old, new)


def make_cumulative(list_: list, cfg) -> None:
    print('\033[96mСоздание кумулятивной сборки ...\033[0m')
    recreate_dir(os.path.join(cfg.cumulative_folder))
    dst_ = f'{cfg.cumulative_folder}\\Client'
    for e in list_:
        src_ = f'{e[1]}\\Client'
        shutil.copytree(src_, dst_, dirs_exist_ok=True)
        print(f'{src_}\t--->\t{dst_}')
    _finish_prepare_cumulative(cfg)
    print('\033[92mКумулятивная сборка создана.\033[0m')
    print()
