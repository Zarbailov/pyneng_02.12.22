# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from pprint import pprint

result_dict = []
with open ('CAM_table.txt') as f:
    for line in f:
        if 'DYNAMIC' in line:
            line = line.split()
            result_dict.append(line)



number_vlan = int(input("Введите номер влана: "))

result_dict_sorted = []
for l in result_dict:
    l[0] = int(l[0])
    if number_vlan == l[0]:
        result_dict_sorted.append(l)
        vlan,mac,state,intf = l
        print("{:>4} {:>17} {:>8}".format(vlan,mac,intf))
