def print_res(wss: dict) -> None:
    def status_formatting(value):
        if value is True:
            return 'Да'
        elif value is False:
            return 'Нет'
        elif value is None:
            return 'N/A'
        else:
            return value

    def _headers_ws():
        headers = ['п/п',
                   'Имя узла',
                   'Доступен',
                   'Та подсеть',
                   'Привилегии',
                   'Есть КЛИЕНТ',
                   'Версия КЛИЕНТ',
                   'Lastfix версия',
                   'Lastfix фикс',
                   'Ставим пакет',
                   'Пакет стоит'
                   ]
        return headers

    def _line_ws(w, n_):
        if not w.client:
            client_ver = None
            client_lastfix_ver = None
            client_lastfix_fix = None
        else:
            client_ver = w.client.ver
            client_lastfix_ver = w.client.lastfix.ver
            client_lastfix_fix = w.client.lastfix.fix
        line = [
                n_,
                w.hostname,
                status_formatting(w.is_available),
                status_formatting(w.is_correct_network),
                status_formatting(w.is_enough_privileges),
                status_formatting(w.is_has_client),
                status_formatting(client_ver),
                status_formatting(client_lastfix_ver),
                status_formatting(client_lastfix_fix),
                status_formatting(w.is_ready_to_fix),
                status_formatting(w.is_fixed),
                ]
        return line

    def ws_print_headers(row: list) -> None:
        print('\033[96m {:^5} | {:^15} | {:^8} | {:^10} | '
              '{:^10} | {:^8} | {:^10} | {:^14} | {:^12} | {:^12} | {:^11} \033[0m'.format(*row))

    def ws_print(row: list) -> None:
        print(' {:^5} | {:<15} | {:^8} | {:^10} | {:^10} | {:^8} | {:<10} | {:<14} | {:^12} | {:^12} | '
              '{:^11} '.format(*row))
    print()
    ws_print_headers(_headers_ws())
    n = 1
    wss_sorted = dict(sorted(wss.items(), key=lambda item: item[0]))
    for ws in wss_sorted.values():
        ws_print(_line_ws(ws, n))
        n += 1
    print()
    print()


def count_res(wss: dict) -> None:
    ok = 0
    for ws in wss.values():
        if ws.is_correct_network is True and ws.is_fixed is True:
            ok += 1
    print()
    print('\033[96mРЕЗУЛЬТАТЫ\033[0m')
    print(f'\033[92m\tВыполнено В ТЕКУЩИХ ПОДСЕТЯХ:\033[0m\t{ok}')
    print(f'\033[91m\tОстальные:\033[0m\t\t\t{len(wss)-ok}')
    print()
    print(f'Выполнение завершено.')
