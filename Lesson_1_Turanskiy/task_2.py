"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

'''Step_1: представление в буквенном формате'''
word_1 = 'class'
word_2 = 'function'
word_3 = 'method'


'''Step_2: проверка типа и содержимого переменных word_1, word_2, word_3'''
print(f'Формат слова {word_1}: ', type(word_1))
print(f'Формат слова {word_2}: ', type(word_2))
print(f'Формат слова {word_3}: ', type(word_3))


'''Step_3: запись слов word_1, word_2, word_3 в байтовом формате'''
word_1_b = b'class'
word_2_b = b'function'
word_3_b = b'method'


'''Step_4: вывод типа, содержимого и длины слов в байтовом формате'''
def byte_format(word, word_b):
    print(f'Слово {word} в байтовом формате имеет вид: {word_b}')
    print(f'Тип: {type(word_b)}')
    print(f'Длина: {len(word_b)}')

byte_format(word_1, word_1_b)
byte_format(word_2, word_2_b)
byte_format(word_3, word_3_b)
