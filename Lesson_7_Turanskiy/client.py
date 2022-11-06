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
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from initial_project.utilities import get_message, send_message
from decorators import log_dec

''' Проводим инициализацию логера клиента '''
CLIENT_LOGGER = logging.getLogger('client_logger')


'''Функция message_from_server обрабатывает сообщения других пользователей, поступающих с сервера'''
@log_dec
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'От пользователя {message[SENDER]} получено сообщение:\n'
              f'{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'От пользователя {message[SENDER]} получено сообщение:\n'
              f'{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'С сервера получено некорректное сообщение: {message}')


'''Функция create_message производит запрос и возврат текста сообщения'''
@log_dec
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение. Для выхода введите \'!out!\': ')
    if message == '!out!' or message == '!OUT!':
        sock.close()
        CLIENT_LOGGER.info('Выход по команде пользователя')
        print('Thank you')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Создан словарь сообщения: {message_dict}')
    return message_dict



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
        elif message[RESPONSE] == 400:
            raise errors.ServerError(f'400 : {message[ERROR]}')
    # return ValueError
    raise errors.ReqFieldMissingError(RESPONSE)


'''Парсер для аргументов командной строки'''
'''После работы парсера возвращается 3 параметра (адрес, порт, режим работы клиента)'''
@log_dec
def create_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # Проверка является ли указанный номер порта подходящим (в диапазоне от 1024 до 65535)
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Запуск с неподходящим номером порта ({server_port}).'
                               f'Выберите порт от 1024 до 65535 включительно')
        sys.exit(1)

    # Проверка является ли указанный режим работы допустимым
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы ({client_mode}).'
                               f'Выберите один из режимов (прослушивание или отправка): listen, send')
        sys.exit(1)

    return server_address, server_port, client_mode


'''Функция main используется для загрузки параметров командной строки'''

def main():
    # Загрузка параметров командной строки
    server_address, server_port, client_mode = create_arguments_parser()

    CLIENT_LOGGER.info(f'Выполнен запуск клиента со следующими параметрами: адрес сервера {server_address}, '
                       f'порт: {server_port}, режим работы клиента: {client_mode}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = server_answer(get_message(transport))
        CLIENT_LOGGER.info(f'Соединение с сервером установлено. Получен ответ от сервера: {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать принятую JSON-строку')
        sys.exit(1)
    except errors.ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера нет поля {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}'
                               f'Конечный компьютер отверг запрос на подключение')
        sys.exit(1)
    except errors.ServerError as error:
        CLIENT_LOGGER.error(f'При попытке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    else:
#         При установке соединения начинаем обмен данными по указанному режиму
        if client_mode == 'send':
            print('Режим работы: отправка сообщений')
        else:
            print('Режим работы: прием сообщений')
        while True:
            # Режим отправки
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} потеряно')
                    sys.exit(1)

            # Режим приема
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} потеряно')
                    sys.exit(1)




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
