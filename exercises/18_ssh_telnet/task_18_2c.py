# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands


import re
from pprint import pprint
import yaml
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

regex = re.compile(
    r"(Invalid input detected .+)"
    r"|(Incomplete command.)"
    r"|(Ambiguous command:)"
)

def send_config_commands(device, config_commands, log=True):
    with ConnectHandler(**device) as ssh:
        if log:
            print(f"Подключаюсь к {device['host']}...")
        ssh.enable()
        dict_without_errors_commands = {}
        dict_with_errors_commands = {}
        for command in config_commands:
            result = ssh.send_config_set(command, exit_config_mode=False)
            match = regex.search(result)
            if match:
                dict_with_errors_commands[command] = result
                print(f"Команда '{command}' выполнилась с ошибокой '{match.group()}' на устройстве {device['host']}")
                accept_error = input("Продолжать выполнят команды? [y]/n: ").lower()
                if accept_error == "no" or accept_error == "n":
                    break
            else:
                dict_without_errors_commands[command] = result
            ssh.exit_config_mode()
        return dict_without_errors_commands, dict_with_errors_commands






if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_config_commands(dev, commands))
        break