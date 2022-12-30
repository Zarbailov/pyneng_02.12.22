# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re


def parse_sh_cdp_neighbors(output):
    regex = re.compile(
        r"(?P<device>\S+) +"
        r"(?P<l_intf>\S+ [0-9]/[0-9]) +\d+.+?"
        r"(?P<port_id>\S+ [0-9]/[0-9])"
    )
    result = {}
    for line in output.split("\n"):
        if "show cdp neighbors" in line:
            hostname = line.split(">")[0]
            result[hostname] = {}
        match = regex.search(line)
        if match:
            device, l_intf, port_id = match.groups()
            result[hostname][l_intf] = {device : port_id}
    return result

if __name__ == "__main__":
    with open(("E:/development/pyneng/17/sh_cdp_n_sw1.txt")) as f:
        pprint(parse_sh_cdp_neighbors(f.read()))
