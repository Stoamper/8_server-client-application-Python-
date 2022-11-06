"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

'''Step_1: создаем список слов в строковом формате'''
words_list = ['разработка', 'администрирование', 'protocol', 'standard']


'''Step_2: перевод каждого из слов в байтовое представление с выводом результатов'''
words_list_b =[]
for i in range(len(words_list)):
    words_list_b.append(words_list[i].encode('utf-8'))
    print(f'Слово {words_list[i]} в байтовом представлении имеет вид {words_list_b[i]}')


'''Step_3: перевод из байтового представления в строковое'''
words_list = []
for i in range(len(words_list_b)):
    words_list.append(words_list_b[i].decode('utf-8'))
    print(f'Слово {words_list_b[i]} в строковом представлении имеет вид {words_list[i]}')