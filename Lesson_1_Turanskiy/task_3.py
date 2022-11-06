"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

'''Step_1: создаем список со словами в строковом типе'''
words_list = ['attribute', 'класс', 'функция', 'type']


'''Step_2: переводим слова из списка в байтовый тип. Если это невозможно выводим исключение'''
for i in range(len(words_list)):
    try:
        word_b = bytes(words_list[i], 'ascii')
        print(f'Слово {words_list[i]} в байтовом формате имеет вид: {word_b}. Его тип: {type(word_b)}')
    except UnicodeEncodeError:
        print(f'Слово {words_list[i]} невозможно записать в байтовом типе. Измените кирилицу на латиницу')



