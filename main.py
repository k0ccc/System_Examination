import PySimpleGUI as sg
import sqlite3

# ПЕРЕМЕННЫЕ
password_static = ''
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
                        sg.Input(size=(30, None)),sg.FileBrowse('Выбрать БД',key='BD_NAME',file_types=(("База sqlite", "*.*"),)), sg.Button('Подключиться')],
                        [sg.Text('Название предмета'),
                        sg.Combo((item),key='item',size=(30, 1)),sg.Button('Выбрать предмет или добавить')],
                        [sg.Text('Вопрос:'), sg.Input(key='answer' ,size=(66, None))],
                        [sg.Text('Создать ответы')],
                        [sg.Input(key='answer_1',size=(16, None)),t_p,sg.Input(key='answer_2',size=(16, None)),t_p,sg.Input(key='answer_3',size=(16, None)),t_p,sg.Input(key='answer_4',size=(16, None))],
                        [sg.Button('Создать')],
                        [sg.Text('Редактирование ответов:')],
                        [sg.Text('Неправильный ответ                      '), sg.Text('  Правильный ответ')],
                        [sg.Combo((question),key='wrong_answer',size=(30, None)), sg.Text('   '),sg.Input(key='ok_answer',size=(25, None)),sg.Button('Редактировать')],
                        [sg.Text('Удалить ответ')],
                        [sg.Combo((delete_question),key='delete_question'),sg.Button('Удалить'), sg.Text('                     '),
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

                # ПОИСК ОТВЕТОВ ДЛЯ "неправильного ответа ответов"
                cursor.execute("SELECT question FROM items")
                question = cursor.fetchall()
                window_main.FindElement('wrong_answer').Update(values=question)
                # ПОИСК ОТВЕТОВ ДЛЯ ""УДАЛИТЬ"
                window_main.FindElement('delete_question').Update(values=question)
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
                if answer_2 == '':
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
                cursor.executemany("INSERT INTO items VALUES (?,?,?)", (request_answer,))
                conn.commit()

                # ПОИСК ОТВЕТОВ ДЛЯ "Редактирование ответов"
                cursor.execute("SELECT question FROM items")
                question = cursor.fetchall()
                window_main.FindElement('wrong_answer').Update(values=question)
                # ПОИСК ОТВЕТОВ ДЛЯ ""УДАЛИТЬ"
                window_main.FindElement('delete_question').Update(values=question)
            # НАЖАТИЕ НА КНОПКУ 'Редактировать'
            if button_main == 'Редактировать':
                # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ
                wrong_answer = values_main['wrong_answer']
                ok_answer = values_main['ok_answer']
                # ЗАПРОС НА ЗАМЕНУ ОТВЕТОВ
                request_edit = [str(ok_answer),str(wrong_answer)]
                cursor.executemany("UPDATE items SET question = (?) WHERE question = (?)",(request_edit,))
                conn.commit()

                # ПОИСК ОТВЕТОВ ДЛЯ "Редактирование ответов"
                cursor.execute("SELECT question FROM items")
                question = cursor.fetchall()
                window_main.FindElement('wrong_answer').Update(values=question)
                # ПОИСК ОТВЕТОВ ДЛЯ ""УДАЛИТЬ"
                window_main.FindElement('delete_question').Update(values=question)
            # ЗАПРОС НА УДАЛЕНИЕ ОТВЕТА
            if button_main == 'Удалить':
                delete_question1 = values_main['delete_question']
                request_delete =[str(delete_question1)]
                cursor.executemany("DELETE FROM items WHERE question = (?)", (request_delete,))
                conn.commit()

                # ПОИСК ОТВЕТОВ ДЛЯ "Редактирование ответов"
                cursor.execute("SELECT question FROM items")
                question = cursor.fetchall()
                window_main.FindElement('wrong_answer').Update(values=question)
                # ПОИСК ОТВЕТОВ ДЛЯ ""УДАЛИТЬ"
                window_main.FindElement('delete_question').Update(values=question)
            # КНОПКА ВЫХОДА
            if button_main is None or button_main == 'Выход':
                quit()
                break
