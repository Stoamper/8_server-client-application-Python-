"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import chardet
from time import sleep


'''Step_1: создадим функцию, которая будет производить ping указанного сайта и вывыодить результаты'''
def site_ping(sitename):
    arguments = ['ping', sitename]
    yandex_ping = subprocess.Popen(arguments, stdout=subprocess.PIPE)
    for line in yandex_ping.stdout:
        answer = chardet.detect(line)
        # Вывод в двоичном формате
        # print(line)
        # Вывод в строковом виде
        print(line.decode(answer['encoding']))

'''Step_2: введем исходные данные, проведем ping. Между выполнением вставим паузу 3 секунды для удобства восприятия'''
site_1 = 'yandex.ru'
site_2 = 'youtube.com'
site_ping(site_1)
sleep(3)
site_ping(site_2)
