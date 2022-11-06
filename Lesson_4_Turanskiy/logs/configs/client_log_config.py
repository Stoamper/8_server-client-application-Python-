'''Конфигурация логгера для клиента'''

import sys
import os
import logging
from initial_project.variables import LOGGING_LEVEL
sys.path.append('../')

# Создание формировщика логов (formatter) (<дата-время> <уровень важности> <имя модуля> <сообщение>)
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Создание имени файла, в который будет осуществляться запись лога
FILE_PATH = os.path.dirname()