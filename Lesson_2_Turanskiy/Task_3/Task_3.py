"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

user_data = {
    'items':
        ['computer', 'printer'],
    'items_quantity': 4,
    'items_price': {
        'computer': '200\u20ac-100\u20ac',
        'printer': '100\u20ac-300\u20ac'
    }
}

with open('file_1.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(user_data, f, allow_unicode=True, sort_keys=False)

with open('file_1.yaml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

print(user_data == data)








