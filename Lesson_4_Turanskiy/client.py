'''Программа-клиент (клентская часть)'''

import sys
import json
import socket
import time
from initial_project.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from initial_project.utilities import get_message, send_message

'''Функция create_presence генерирует запрос о присутствии клиент'''


def create_presence(account_name='Guest'):
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    output = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return output


'''Функция server_answer разбирает ответ сервера (ОК - 200, НЕ ОК - 400)'''


def server_answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "The HTTP 200 OK"
        return f'400 : {message[ERROR]}'
    return ValueError


'''Функция main используется для загрузки параметров командной строки'''


def main():
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


if __name__ == '__main__':
    main()
