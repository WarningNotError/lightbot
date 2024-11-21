import sqlite3
import telebot, time
from telebot import types
import linecache
import subprocess

bot = telebot.TeleBot("6641930957:AAGreK3KRnSI2G-PbKmT-uZdLPReir3wCq4")

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

@bot.message_handler(commands=['start'])
def start_message(message):
    # markup=types.InlineKeyboardMarkup()
    # item1=types.InlineKeyboardButton("О нас", url = 'https://lightcom.msk.ru/')
    # markup.row(item1)
    # bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}! Я LightCom_Bot!', reply_markup=markup)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Подробная спецификация")
    btn2 = types.KeyboardButton("Добавить данные")
    btn3 = types.KeyboardButton("Найти заказ в базе")
    markup.add(btn1, btn2, btn3)

    msg = bot.send_message(message.chat.id, f'Выбери, что хочешь', reply_markup=markup)

    bot.register_next_step_handler(msg, whatismsg)

def whatismsg(message):
    choose_msg = message.text  # Это и будет текст, который отправил пользователь

    if choose_msg == 'Найти заказ в базе':
        bot.send_message(message.chat.id, text=choose_msg.format(message.from_user), reply_markup=types.ReplyKeyboardRemove())
        find(message)

    if choose_msg == 'Добавить данные':
        bot.send_message(message.chat.id, text=choose_msg.format(message.from_user), reply_markup=types.ReplyKeyboardRemove())
        add_start(message)

    if choose_msg == 'Подробная спецификация':
        bot.send_message(message.chat.id, text=choose_msg.format(message.from_user), reply_markup=types.ReplyKeyboardRemove())
        spec(message)

@bot.message_handler(commands=['find'])
def find(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Номер заказа")
    btn2 = types.KeyboardButton("Модель монитора")
    btn3 = types.KeyboardButton("Серийный номер")
    btn4 = types.KeyboardButton("Имя заказчика")
    btn5 = types.KeyboardButton("Назад")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    msg = bot.send_message(message.chat.id, text="Выбери по каким данным хочешь найти.".format(message.from_user), reply_markup=markup)

    # msg = bot.send_message(message.chat.id, 'Введите ник для поиска сообщений:')
    bot.register_next_step_handler(msg, input_msg)

# Интерпритация параметра, по которому ищем
def input_msg(message):
    choose_msg = message.text  # Это и будет текст, который отправил пользователь
    bot.delete_message(message.chat.id,message.message_id)
    
    if choose_msg == 'Номер заказа':
        msg = bot.send_message(message.chat.id, text="Введи номер заказа".format(message.from_user), reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_n_zakaza)
    
    if choose_msg == 'Серийный номер':
        msg = bot.send_message(message.chat.id, text="Введи серийный номер".format(message.from_user), reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_sn)
    
    if choose_msg == 'Модель монитора':
        bot.send_message(message.chat.id, f'Данная функция пока в разработке')
        find(message)
    
    if choose_msg == 'Имя заказчика':
        bot.send_message(message.chat.id, f'Данная функция пока в разработке')
        find(message)

    if choose_msg == 'Назад':
        bot.send_message(message.chat.id, f'Данная функция пока в разработке')
        start_message(message)

# Если поиск будет по номеру заказа
def input_n_zakaza(message):
    choose_msg = message.text # Это и будет текст, который отправил пользователь
    bot.delete_message(message.chat.id,message.message_id)
    
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Zakazi WHERE N_zakaza LIKE "' + choose_msg + '"')
    results = cursor.fetchall()
    numrows = len(results)

    if numrows < 1:
        bot.send_message(message.chat.id, 'Заказа <b>' + choose_msg + '</b> нет в базе данных', parse_mode="HTML")
        return start_message(message)
    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Заказ <b>' + results[numrows-1][0] + '</b> серийный номер <b>' + results[numrows-1][1] + '</b> гарантия <b>' + results[numrows-1][3] + '</b>\n'
        numrows -= 1

    bot.send_message(message.chat.id, f'{"".join(mass_result)}', parse_mode="HTML")
        
    connection.close()
    start_message(message)
# Если поиск будет по серийному номеру
def input_sn(message):
    choose_msg = message.text # Это и будет текст, который отправил пользователь

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Zakazi WHERE SN LIKE "' + choose_msg + '"')
    results = cursor.fetchall()
    numrows = len(results)

    if numrows < 1:
        bot.send_message(message.chat.id, 'Серийного номера ' + choose_msg + ' нет в базе данных')
        return
    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Заказ <b>' + results[numrows-1][0] + '</b> серийный номер <b>' + results[numrows-1][1] + '</b> гарантия <b>' + results[numrows-1][3] + '</b>\n'
        numrows -= 1

    bot.send_message(message.chat.id, f'{"".join(mass_result)}', parse_mode="HTML")
        
    connection.close()
    start_message(message)

@bot.message_handler(commands=['add'])
def add_start(message):

    msg = bot.send_message(message.chat.id, text="Чтобы добавить данные введи номер заказа".format(message.from_user))
    bot.register_next_step_handler(msg,add_n_zakaza)

def add_n_zakaza(message):
    bot.delete_message(message.chat.id,message.message_id)
    global n_zakaza
    n_zakaza= message.text  # Это и будет текст, который отправил пользователь
    msg = bot.send_message(message.chat.id, text="Введите серийный номер".format(message.from_user))
    bot.register_next_step_handler(msg,add_sn)

def add_sn(message):
    bot.delete_message(message.chat.id,message.message_id)
    global sn
    sn = message.text  # Это и будет текст, который отправил пользователь

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM Zakazi WHERE SN LIKE "' + sn + '"')
    results = cursor.fetchall()
    # bot.send_message(message.chat.id, str(results))
    if str(results) != '[]':
        bot.send_message(message.chat.id, "Такой серийный номер уже используется в дргуом заказе")
        connection.close()
        return

    connection.close()

    msg = bot.send_message(message.chat.id, text="Введите дату заказа".format(message.from_user))
    bot.register_next_step_handler(msg,add_date)

def add_date(message):
    bot.delete_message(message.chat.id,message.message_id)
    global date
    date = message.text  # Это и будет текст, который отправил пользователь
    msg = bot.send_message(message.chat.id, text="Введите длительность гарантии".format(message.from_user))
    bot.register_next_step_handler(msg,add_war)

def add_war(message):
    bot.delete_message(message.chat.id,message.message_id)
    global war
    war = message.text  # Это и будет текст, который отправил пользователь
    ans = 'Номер заказа ' + n_zakaza + ' серийный номер ' + sn + ' дата ' + date + ' гарантия ' + war + '\n'
    bot.send_message(message.chat.id, ans.format(message.from_user), parse_mode="HTML")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    btn3 = types.KeyboardButton("Затрудняюсь ответить")
    markup.add(btn1, btn2, btn3)

    msg = bot.send_message(message.chat.id, text = "Данные верны? Ответьте Да/Нет", parse_mode="HTML", reply_markup=markup)

    bot.register_next_step_handler(msg,add_end)

def add_end(message):
    bot.delete_message(message.chat.id,message.message_id)
    if message.text == 'Да':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Zakazi (N_zakaza, SN, Date, Warranty) VALUES (?, ?, ?, ?)', (n_zakaza, sn, date, war))

        connection.commit()
        connection.close()
        bot.send_message(message.chat.id, "Данные внесены", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        msg = bot.send_message(message.chat.id, text = "Не спешт отвечать, подумай еще.\n Данные верны? Ответьте Да/Нет", parse_mode="HTML")
        bot.register_next_step_handler(msg,add_end)
    start_message(message)
# Кнопка подробной спецификации
@bot.message_handler(commands=['spec'])
def spec(message):
    markup=types.InlineKeyboardMarkup()
    item1=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.100", callback_data='LightCom V-Lite-S ПЦВТ.852859.100')
    item2=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.100-02", callback_data='LightCom V-Lite-S ПЦВТ.852859.100-02')
    item3=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.200", callback_data='LightCom V-Lite-S ПЦВТ.852859.200')
    item4=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.200-01", callback_data='LightCom V-Lite-S ПЦВТ.852859.200-01')
    item5=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.200-04", callback_data='LightCom V-Lite-S ПЦВТ.852859.200-04')
    item6=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.200-05", callback_data='LightCom V-Lite-S ПЦВТ.852859.200-05')
    item7=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.300", callback_data='LightCom V-Lite-S ПЦВТ.852859.300')
    item8=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.300-02", callback_data='LightCom V-Lite-S ПЦВТ.852859.300-02')
    item9=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.300-04", callback_data='LightCom V-Lite-S ПЦВТ.852859.300-04')
    item10=types.InlineKeyboardButton("LightCom V-Lite-S ПЦВТ.852859.300-05", callback_data='LightCom V-Lite-S ПЦВТ.852859.300-05')
    item11=types.InlineKeyboardButton("LightCom V-Plus 24 ПЦВТ.852859.400", callback_data='LightCom V-Plus 24 ПЦВТ.852859.400')
    item12=types.InlineKeyboardButton("LightCom V-Plus 24 ПЦВТ.852859.400-04", callback_data='LightCom V-Plus 24 ПЦВТ.852859.400-04')
    markup.row(item1)
    markup.row(item2)
    markup.row(item3)
    markup.row(item4)
    markup.row(item5)
    markup.row(item6)
    markup.row(item7)
    markup.row(item8)
    markup.row(item9)
    markup.row(item10)
    markup.row(item11)
    markup.row(item12)

    bot.send_message(message.chat.id, f'Наименования мониторов, по которым представлена спецификация:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.100')
def save_btn1(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.100-02')
def save_btn2(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.200')
def save_btn3(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.200-01')
def save_btn4(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.200-04')
def save_btn5(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.200-05')
def save_btn6(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.300')
def save_btn7(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.300-02')
def save_btn8(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.300-04')
def save_btn9(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Lite-S ПЦВТ.852859.300-05')
def save_btn10(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Plus 24 ПЦВТ.852859.400')
def save_btn11(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'LightCom V-Plus 24 ПЦВТ.852859.400-04')
def save_btn12(call):

    message = call.message
    chat_id = message.chat.id

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Spec WHERE name LIKE "' + call.data + '"')
    results = cursor.fetchall()
    numrows = len(results)

    mass_result = [0] * numrows

    while numrows>0:
        mass_result[numrows-1] = 'Название <b>' + results[numrows-1][0] + '</b>\n Номер в реестрах <b>' + results[numrows-1][1] + '</b>\n Тип матрицы <b>' + results[numrows-1][2] + '</b>\n Размер видимой области дисплея <b>' + results[numrows-1][3] + '</b>\n Разрешение <b>' + results[numrows-1][4] + '</b>\n Плотность пикселей <b>' + results[numrows-1][5] + '</b>\n Соотношение сторон <b>' + results[numrows-1][6] + '</b>\n Типичная яркость <b>' + results[numrows-1][7] + '</b>\n Максимальная яркость <b>' + results[numrows-1][8] + '</b>\n Контрастность <b>' + results[numrows-1][9] + '</b>\n Динамическая контрастность <b>' + results[numrows-1][10] + '</b>\n Время отклика <b>' + results[numrows-1][11] + '</b>\n Углы обзора по гориз/вертик <b>' + results[numrows-1][12] + '</b>\n Частота обновления экрана <b>' + results[numrows-1][13] + '</b>\n Частота обновления экрана при FullHD <b>' + results[numrows-1][14] + '</b>\n Снижение нагрузки на зрение <b>' + results[numrows-1][15] + '</b>\n Количество цветов <b>' + results[numrows-1][16] + '</b>\n Цветовой охват <b>' + results[numrows-1][17] + '</b>\n Подсветка экрана <b>' + results[numrows-1][18] + '</b>\n Покрытие диспея <b>' + results[numrows-1][19] + '</b>\n Видео разъемы <b>' + results[numrows-1][20] + '</b>\n Поддержка HDCP <b>' + results[numrows-1][21] + '</b>\n USB-порты <b>' + results[numrows-1][22] + '</b>\n Чтение карт памяти <b>' + results[numrows-1][23] + '</b>\n Аудио-разъемы <b>' + results[numrows-1][24] + '</b>\n Звук <b>' + results[numrows-1][25] + '</b>\n Веб-камера <b>' + results[numrows-1][26] + '</b>\n Регулеравка наклона <b>' + results[numrows-1][27] + '</b>\n Регулеровка высоты <b>' + results[numrows-1][28] + '</b>\n Поворот по горизонтали <b>' + results[numrows-1][29] + '</b>\n Портретный режим <b>' + results[numrows-1][30] + '</b>\n Размер крепления VESA <b>' + results[numrows-1][31] + '</b>\n Блок питания <b>' + results[numrows-1][32] + '</b>\n Максимальная потребляемая мощность <b>' + results[numrows-1][33] + '</b>\n Класс энергоэффективности <b>' + results[numrows-1][34] + '</b>\n Цвет корпуса <b>' + results[numrows-1][35] + '</b>\n Разъем Kensington Lock <b>' + results[numrows-1][36] + '</b>\n Размеры с подставкой (Ш*В*Г) <b>' + results[numrows-1][37] + '</b>\n Масса нетто/брутто <b>' + results[numrows-1][38] + '</b>\n Размеры упаковки (Ш*В*Г) <b>' + results[numrows-1][39] + '</b>\n Станд/расшир гарантия <b>' + results[numrows-1][40] + '</b>\n'
        numrows -= 1

    bot.send_message(chat_id, f'{"".join(mass_result)}', parse_mode="HTML")

    connection.close()
    start_message(message)

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    
    cursor.execute('INSERT INTO Users (username, message, time) VALUES (?, ?, ?)', 
               (message.from_user.first_name, message.text, tconv(message.date)))
    connection.commit()
    connection.close()

bot.infinity_polling(timeout=10, long_polling_timeout = 5)