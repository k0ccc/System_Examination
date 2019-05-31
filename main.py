import PySimpleGUI as sg
import sqlite3

# ПЕРЕМЕННЫЕ
password_static = ''
item = []
window_main_bool = False

login = [[sg.Text('Пароль?', font='Colibri 15')],
        [sg.Input(key='password',password_char='*', font='Colibri 15',size=(15, None))],
        [sg.Button('Ок'),sg.Button('Выход')]
        ]

window_pas = sg.Window('Вход',login)

while True:
    button_pas, values_pas = window_pas.Read()

    if button_pas is None or button_pas == 'Выход':
        break
    password = values_pas['password']
    if password == password_static and button_pas == 'Ок' and not window_main_bool:

        window_pas.Hide()
        window_main_bool = True
        t_p = sg.Text('*')
        # ИНТЕРФЕЙС 2 ОКНА ПОСЛЕ ПОРОЛЯ
        win_main_lay = [
                        [sg.Text('Название БД:  '),
                        sg.Input(size=(30, None)),sg.FileBrowse('Выбрать БД',key='BD_NAME',file_types=(("База sqlite", "*.*"),)), sg.Button('Подключиться')],
                        [sg.Text('Название предмета'),
                        sg.Combo(('Выберете предмет',item),key='item',readonly=True, size=(20, 1)),
                        sg.Button('Выбрать предмет')],
                        [sg.Text('Вопрос:'), sg.Input(key='answer' ,size=(66, None))],
                        [sg.Text('Создать ответы')],
                        [sg.Input(key='answer_1',size=(16, None)),t_p,sg.Input(key='answer_2',size=(16, None)),t_p,sg.Input(key='answer_3',size=(16, None)),t_p,sg.Input(key='answer_4',size=(16, None))],
                        [sg.Button('Создать')],
                        [sg.Text('Редактирование ответов:')],
                        [sg.Text('Неправильный ответ  '), sg.Text('  Правильный ответ')],
                        [sg.Input(key='wrong_answer',size=(16, None)), sg.Text('   '),sg.Input(key='ok_answer',size=(16, None)),sg.Button('Редактировать')],
                        [sg.Text('Удалить ответ')],
                        [sg.Input(key='delete_anwser'),sg.Button('Удалить'), sg.Text('                     '),
                        sg.Button('Выход')]
                        ]
        window_main = sg.Window('Test',win_main_lay)
        while True:
            # ПЕРЕМЕННЫЕ
            button_main, values_main = window_main.Read(timeout=100)

            # НАЖАТИЕ НА КНОПКУ 'Подключиться'
            if button_main == 'Подключиться':
                # ПОДКЛЮЧЕНИЕ К БД
                BD_NAME = values_main['BD_NAME']
                conn = sqlite3.connect(BD_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT item FROM items")
                item = cursor.fetchall()
                window_main.FindElement('item').Update(values=item)
                print("Подключился к бд вывел, список предметов:" + str(item))

            if button_main == 'Выбрать предмет':
                item = values_main['item']

            if button_main == 'Создать':
                answer = values_main['answer']
                answer_1 = values_main['answer_1']
                answer_2 = values_main['answer_2']
                answer_3 = values_main['answer_3']
                answer_4 = values_main['answer_4']
                # ЗАПРОС К БД НА СОЗДАНИЕ ВОПРОСА С ОТВЕТАМИ
                request_answer =    [
                            (item,answer , answer_1),
                            (item, answer, answer_2),
                            (item, answer, answer_3),
                            (item, answer, answer_4)
                                    ]

                cursor.executemany("INSERT INTO items VALUES (?,?,?)", request_answer)
                conn.commit()

            if button_main is None or button_main == 'Выход':
                quit()
                break
