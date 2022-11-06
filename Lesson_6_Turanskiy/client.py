"""Программа-клиент (клентская часть)"""

import argparse
import logging
import sys
import json
import socket
import time
import errors
import logs.configs.client_log_config
from initial_project.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from initial_project.utilities import get_message, send_message
from decorators import log_dec

''' Проводим инициализацию логера клиента '''
CLIENT_LOGGER = logging.getLogger('client_logger')



'''Функция create_presence генерирует запрос о присутствии клиент'''

@log_dec
def create_presence(account_name='Guest'):
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    output = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Для пользователя {account_name} сформировано {PRESENCE} сообщение')
    return output


'''Функция server_answer разбирает ответ сервера (ОК - 200, НЕ ОК - 400)'''

@log_dec
def server_answer(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "The HTTP 200 OK"
        return f'400 : {message[ERROR]}'
    # return ValueError
    raise errors.ReqFieldMissingError(RESPONSE)


'''Парсер для аргументов командной строки'''
@log_dec
def create_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


'''Функция main используется для загрузки параметров командной строки'''

def main():
    parser = create_arguments_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # Проверка номера порта на правильность
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Обнаружена попытка запуска клиента с неправильным номером порта: {server_port}. '
            f'Допустимые адреса с 1024 по 65535 включительно')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Параметры запущенного клиента: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = server_answer(get_message(transport))
        CLIENT_LOGGER.info(f'Получен ответ от сервера: {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать принятую JSON-строку')
    except errors.ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера нет поля {missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}')





'''
# До 5 урока
    # client.py 192.168.0.24 8079
    # server.py -p 8079 192.168.0.24
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError('Номер порта не в диапазоне от 1024 до 65535')
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Номер порта не в диапазоне от 1024 до 65535')
        sys.exit(1)

    # Проводим инициализацию и обмен
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = server_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удается декодировать сообщение сервера')
'''

if __name__ == '__main__':
    main()
