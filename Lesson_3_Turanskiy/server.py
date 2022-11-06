'''Программа-сервер (серверная часть)'''

import sys
import json
import socket
from initial_project.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from initial_project.utilities import get_message, send_message

'''Функция process_client_message является обработчиком сообщений от клиентов'''
'''Принимает сообщение от клиента (словарь), проверяет его валидность, возвращает ответ для клиента (также словарь)'''


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }


'''Функция main используется для загрузки параметров командной строки'''
'''Если нет параметров, то задаем значения по умолчанию (DEFAULT_PORT)'''
'''Первоначально обрабатываем порт: server.py -p 8079 -a 192.168.1.2'''


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError('Значение порта вне допустимого диапазона (должно быть от 1024 до 65535)')
    except IndexError:
        print('После параметра -\'p\' следует указать номер порта')
        sys.exit(1)
    except ValueError:
        print('Значение порта вне допустимого диапазона (должно быть от 1024 до 65535)')
        sys.exit(1)

    # Загружаем адрес, который будем слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print('После параметра -\'a\' необходимо указать адрес, который будет слушать сервер')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Получено некорректное сообщение от клиента')
            client.close()

if __name__ == '__main__':
    main()
