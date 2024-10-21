import telegram

bot = telegram.Bot(token='7030442780:AAGrNsidCIUmR6XDaGC0y1WSNEwKa4Vsdjw')

print(bot.get_me())

chat_id = '-1002280010724'  # Замените на настоящий ID чата

bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")