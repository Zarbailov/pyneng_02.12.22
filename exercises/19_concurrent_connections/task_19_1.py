# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping(ip):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            encoding='utf-8'
    )
    return {ip : reply.returncode}







def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping, ip_list)
        for ip_dict in result:
            for keys, values in ip_dict.items():
                if values == 0:
                    reachable.append(keys)
                else:
                    unreachable.append(keys)
    return reachable, unreachable


ip_addr = ["10.20.30.40", "8.8.8.8",
           "11.22.33.44", "192.168.100.1",
           "192.168.100.2", "192.168.100.3"]

if __name__ == "__main__":
    print(ping_ip_addresses(ip_addr))
