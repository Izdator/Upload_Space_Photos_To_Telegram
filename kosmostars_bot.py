import telegram
import os
import argparse
from dotenv import load_dotenv


def main(file_path):
    load_dotenv()

    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(token)
    bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")

    with open(file_path, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a file to a Telegram chat.")
    parser.add_argument('file_path', type=str, help='The path to the file to be sent.')

    args = parser.parse_args()

    main(args.file_path)
