import sqlite3
import lightbot

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# cursor.execute(' INTO Users (username, email, age) VALUES (?, ?, ?)', 
#                ('newuer', lightbot.message.from_user.first_name, 40))
  
# Выбираем имена и возраст пользователей старше 25 лет
# cursor.execute('SELECT * FROM Users')
# results = cursor.fetchall()

# f = open('testbd','r+')

# f.write(str(results))



# f.close()
connection.commit()
connection.close()
