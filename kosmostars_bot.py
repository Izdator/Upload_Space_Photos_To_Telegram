import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')

    bot = telegram.Bot(token)
    bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")

    relative_path = 'images/nasa_apod_20240922.jpg'
    file_path = os.path.join(os.getcwd(), relative_path)

    with open(file_path, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)


if __name__ == "__main__":
    main()
