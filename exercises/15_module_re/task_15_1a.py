# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re
#variant 1
def get_ip_from_cfg(filename):
    with open(filename) as f:
        result = {}
        for line in f:
            if line.startswith("interface"):
                intf = re.search(r"interface (?P<intf>\S+)", line).group("intf")
            elif line.startswith(" ip address"):
                match = re.search("ip address (?P<ip>[\d.]+) (?P<mask>[\d.]+)", line)
                result[intf] = match.groups()
    return result
                
if __name__ == "__main__":
    print(get_ip_from_cfg("E:/development/pyneng/15/config_r1.txt"))

#variant 2
def get_ip_from_cfg(filename):
    regex = (r"interface (?P<intf>\S+)"
        r"|ip address (?P<ip>[\d.]+) (?P<mask>[\d.]+)"
    )
    with open(filename) as f:
        result = {}
        for line in f:
            match = re.search(regex, line)
            if match:
                if match.lastgroup == "intf":
                    intf = match.group(match.lastgroup)
                else:
                    result[intf] = match.group("ip", "mask")
        return result

if __name__ == "__main__":
    print(get_ip_from_cfg("E:/development/pyneng/15/config_r1.txt"))
