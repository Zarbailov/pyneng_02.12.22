# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re

def get_ints_without_description(filename):
    with open(filename) as f:
        result = []
        regex = (r'^interface (?P<intf>\S+)'
                r'|(?P<descr>^ description)')
        for line in f:
            match = re.search(regex,line)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group('intf')
                    result.append(intf)
                else:
                    result.remove(intf)
        return result


if __name__ == "__main__":
    pprint(get_ints_without_description("E:/development/pyneng/15/config_r1.txt"))
