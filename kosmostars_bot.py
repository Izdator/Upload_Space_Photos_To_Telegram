import telegram
import os
from dotenv import load_dotenv


load_dotenv()


token = os.environ.get('TELEGRAM_TOKEN')

chat_id = os.environ.get('CHAT_ID')


bot = telegram.Bot(token)


def main():

    bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")

    with open('C:\\Users\\79647\\Desktop\\Upload_Space_Photos_To_Telegram\\images\\nasa_apod_20240922.jpg', 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)


if __name__ == "__main__":
    main()
