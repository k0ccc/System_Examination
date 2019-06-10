import PySimpleGUI as sg
import sqlite3
from xlwt import *
import sys
import os

# ПЕРЕМЕННЫЕ
# для создания листов в .xls
f = 0
# пароль для входа
password_static = ''
w = Workbook()
item = ['Выберете предмет или добавте его']
question = ['Выберете неправильный ответ']
delete_question = ['Выберете ответ который надо удалить']
window_main_bool = False
# Инетерфейс пороля
login = [[sg.Text('Пароль?', font='Colibri 15')],
        [sg.Input(key='password',password_char='*', font='Colibri 15',size=(15, None))],
        [sg.Button('Ок'),sg.Button('Выход')]
        ]

window_pas = sg.Window('Вход',login)

def request():
    # ПОИСК ОТВЕТОВ ДЛЯ "Редактирование ответов"
    cursor.execute("SELECT question FROM items")
    question = cursor.fetchall()
    window_main.FindElement('wrong_answer').Update(values=question)
    # ПОИСК ОТВЕТОВ ДЛЯ ""УДАЛИТЬ"
    window_main.FindElement('delete_question').Update(values=question)

while True:
    # Чтение конпок и полей
    button_pas, values_pas = window_pas.Read()
    # Нажатие на кнопку выход
    if button_pas is None or button_pas == 'Выход':
        break
    password = values_pas['password']
    # Сравнение пароля с паролем записаным в программе и нажатие кнопки "Ок"
    if password == password_static and button_pas == 'Ок' and not window_main_bool:
        # Скрытие окна с паролем
        window_pas.Hide()
        window_main_bool = True
        # Переменная
        t_p = sg.Text('*')
        # ИНТЕРФЕЙС 2 ОКНА ПОСЛЕ ПОРОЛЯ
        win_main_lay = [
                        [sg.Text('Название БД:  '),
                        sg.Input(size=(30, 1)),
                        sg.FileBrowse('Выбрать БД',key='BD_NAME',
                        file_types=( ("База sqlite", "*.*"),)),
                        sg.Button('Подключиться')],
                        [sg.Text('Название предмета'),
                        sg.Combo((item),key='item',size=(30, 1)),
                        sg.Button('Выбрать предмет или добавить')],
                        [sg.Text('Вопрос:'),
                        sg.Input(key='answer' ,size=(66, 1))],
                        [sg.Text('Создать ответы')],
                        [sg.Input(key='answer_1',size=(16, 1)),
                        t_p,
                        sg.Input(key='answer_2',size=(16, 1)),
                        t_p,
                        sg.Input(key='answer_3',size=(16, 1)),
                        t_p,
                        sg.Input(key='answer_4',size=(16, 1))],
                        [sg.Button('Создать')],
                        [sg.Text('Редактирование ответов:')],
                        [sg.Text('Неправильный ответ                      '), sg.Text('           Правильный ответ')],
                        [sg.Combo((question),key='wrong_answer',size=(30, 1)),
                        sg.Text('   '),
                        sg.Input(key='ok_answer', size=(25, 1)),
                        sg.Button('Редактировать')],
                        [sg.Text('Удалить ответ')],
                        [sg.Combo((delete_question),key='delete_question'),
                        sg.Button('Удалить'),
                        sg.Text('      '),
                        sg.B('Вывести всё в xls'),
                        sg.Button('Выход')]
                        ]
        window_main = sg.Window('Test',win_main_lay)
        while True:
            # Чтение конпок и полей
            button_main, values_main = window_main.Read(timeout=100)

            # НАЖАТИЕ НА КНОПКУ 'Подключиться'
            if button_main == 'Подключиться':
                # ПОДКЛЮЧЕНИЕ К БД
                BD_NAME = values_main['BD_NAME']
                conn = sqlite3.connect(BD_NAME)
                cursor = conn.cursor()
                # Запрос на вывод всех предметов из БД
                cursor.execute("SELECT DISTINCT item FROM items")
                # Присваивание всех предметов item
                item = cursor.fetchall()
                # Обновление поля "Выберете предмет или добавте его"
                window_main.FindElement('item').Update(values=item)
                # Вызов функции "request()""
                request()
                item = values_main['item']
                answer = values_main['answer']
            # НАЖАТИЕ НА КНОПКУ 'Выбрать предмет или добавить'
            if button_main == 'Выбрать предмет или добавить':
                item = values_main['item']
            # НАЖАТИЕ НА КНОПКУ 'Создать'
            if button_main == 'Создать':
                answer = values_main['answer']
                answer_1 = values_main['answer_1']
                answer_2 = values_main['answer_2']
                answer_3 = values_main['answer_3']
                answer_4 = values_main['answer_4']
                # Проверка на пустые поля
                if answer_1 == '':
                    pass
                elif answer_2 == '':
                    request_answer =    [
                                (str(item), str(answer), str(answer_1))]
                elif answer_3 == '':
                    request_answer =    [
                                (str(item), str(answer), str(answer_1)),
                                (str(item), str(answer), str(answer_2))]
                elif answer_4 == '':
                    request_answer =    [
                                (str(item), str(answer), str(answer_1)),
                                (str(item), str(answer), str(answer_2)),
                                (str(item), str(answer), str(answer_3))]
                else:
                    request_answer =    [
                                (str(item), str(answer), str(answer_1)),
                                (str(item), str(answer), str(answer_2)),
                                (str(item), str(answer), str(answer_3)),
                                (str(item), str(answer), str(answer_4))
                                        ]
                # ЗАПРОС К БД НА СОЗДАНИЕ ВОПРОСА С ОТВЕТАМИ
                cursor.executemany("INSERT INTO items VALUES (?,?,?)", (request_answer))
                conn.commit()
                # Вызов функции "request()"
                request()
            # НАЖАТИЕ НА КНОПКУ 'Редактировать'
            if button_main == 'Редактировать':
                # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ
                wrong_answer = values_main['wrong_answer']
                ok_answer = values_main['ok_answer']
                # ЗАПРОС НА ЗАМЕНУ ОТВЕТОВ
                request_edit = [str(ok_answer),str(wrong_answer)]
                cursor.executemany("UPDATE items SET question = (?) WHERE question = (?)",(request_edit,))
                conn.commit()
                # Вызов функции "request()""
                request()
            # ЗАПРОС НА СОЗДАНИЕ .XLS ТАБЛИЦЫ СО ВСЕМИ ДАННЫМИ
            if button_main == 'Вывести всё в xls':
                cursor.execute("SELECT item FROM items")
                item = cursor.fetchall()
                cursor.execute("SELECT question FROM items")
                question = cursor.fetchall()
                cursor.execute("SELECT answer FROM items")
                answer = cursor.fetchall()
                ws = w.add_sheet(str(f))
                if os.path.isfile('./items.xls') == True:
                    f += 1
                    os.remove('items.xls')
                    ws.write(0,1, 'Предмет')
                    ws.write(0,2, 'Вопрос')
                    ws.write(0,3, 'Ответ')
                    i = 1
                    print(item,answer,question)
                    for ite,answe,questio in list(zip(item,answer,question)):
                        ws.write(i, 1, ite)
                        ws.write(i, 2, answe)
                        ws.write(i, 3, questio)
                        i += 1
                    w.save('items.xls')
                else:
                    f += 1
                    ws.write(0,1, 'Предмет')
                    ws.write(0,2, 'Вопрос')
                    ws.write(0,3, 'Ответ')
                    i = 1
                    print(item,answer,question)
                    for ite,answe,questio in list(zip(item,answer,question)):
                        ws.write(i, 1, ite)
                        ws.write(i, 2, answe)
                        ws.write(i, 3, questio)
                        i += 1
                    w.save('items.xls')

            # ЗАПРОС НА УДАЛЕНИЕ ОТВЕТА
            if button_main == 'Удалить':
                delete_question1 = values_main['delete_question']
                request_delete =[str(delete_question1)]
                cursor.executemany("DELETE FROM items WHERE question = (?)", (request_delete,))
                conn.commit()
                # Вызов функции "request()""
                request()
            # КНОПКА ВЫХОДА
            if button_main is None or button_main == 'Выход':
                sys.exit(0)
