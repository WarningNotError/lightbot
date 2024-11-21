import telebot
from telebot import types
import linecache


bot = telebot.TeleBot("6641930957:AAGreK3KRnSI2G-PbKmT-uZdLPReir3wCq4")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Вас приветсвует светобот")

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
	testbd = open('testbd', 'r+')
	ans = open('answer', 'r+')
	message_from_user = message.text
	line_number = 1 #номер строки
	desired_line = linecache.getline('testbd', line_number).strip() #desired_line - строка из файла
	
	if message_from_user == "Ну че там":
		bot.send_message(message.chat.id, desired_line)
		testbd.close()
	else:
		bot.reply_to(message, ans)
		ans.close()

bot.polling()