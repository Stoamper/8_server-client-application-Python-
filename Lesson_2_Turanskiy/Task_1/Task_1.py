"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

'''Step_1: создание функции get_data(), осуществляющей чтение и извлечение данных'''
import re
import csv

def get_data(filename):
    try:
        with open(filename, 'r') as f:
            for line in f:
                if re.match(r'Изготовитель системы', line):
                    os_prod_list.append(line.split(':')[-1].replace(' ', '').replace('\n', ''))
                    # print(os_prod_list)
                elif re.match(r'Название ОС', line):
                    os_name_list.append(' '.join((line.split('Microsoft')[-1]).split(' ')[1:3]))
                elif re.match(r'Код продукта', line):
                    os_code_list.append(line.split(':')[-1].replace(' ', '').replace('\n', ''))
                elif re.match(r'Тип системы', line):
                    os_type_list.append(line.split(':')[-1].replace(' ', '').replace('\n', ''))

    except FileNotFoundError:
        print(f'Файла {filename} не существует. Проверьте введенные данные')

'''Step_2: обработка функцией исходных файлов, получение списков с данными'''
main_data = []
column_names = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
main_data.append(column_names)
os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
get_data('info_1.txt')
get_data('info_2.txt')
get_data('info_3.txt')

'''Step_3: формирование списка с итоговыми данными, который будет выводится в csv-файл'''
for i in range(len(column_names) - 1):
    info = [i + 1, os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]]
    main_data.append(info)

'''Step_4: функция формирование окончательного csv-файла с информацией'''
def write_to_csv(file):
    with open('data_report_1.csv', 'w', newline='', encoding='utf-8') as f:
        f_writer = csv.writer(f)

        for row in file:
            f_writer.writerow(row)

write_to_csv(main_data)