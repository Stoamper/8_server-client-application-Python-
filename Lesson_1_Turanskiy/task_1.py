"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции

ВНИМАНИЕ!!: сдача задания
1) создать папку Lesson_1_Ivanov
2) в папку положить файлы task_1 - task_6 (а также txt-файл для последнего)
3) заархивировать папку! и сдать архив

Все другие варианты сдачи приму только один раз, потом буду ставить НЕ СДАНО
"""

'''Step_1: представление в буквенном формате'''
word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'


'''Step_2: проверка типа и содержимого переменных word_1, word_2, word_3'''
print(f'Формат слова {word_1}: ', type(word_1))
print(f'Формат слова {word_2}: ', type(word_2))
print(f'Формат слова {word_3}: ', type(word_3))


'''Step_3: преобразование строки в набор кодовых точек'''
'''В функции получаем значения символов в шестнадцатеричном виде и добавляем символ \\u для правильно отображения'''
'''Итог работы функции: представление исходного слова как набора кодовых точек, вывод формата'''
def word_to_code_point(word):
    word_cp = ''
    for i in range(len(word)):
        letter_hex = '\\u' + hex(ord(word[i]))[0:1] + hex(ord(word[i]))[2:]
        word_cp = word_cp + letter_hex
    print(f'Предстваление слова {word} в виде кодовых точек: {word_cp}')
    print(f'Тип представления в виде кодовых точек: {type(word_cp)}')

word_to_code_point(word_1)
word_to_code_point(word_2)
word_to_code_point(word_3)