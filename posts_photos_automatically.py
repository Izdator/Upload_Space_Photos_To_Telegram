import argparse
import os
import random
import telegram
from dotenv import load_dotenv
from time import sleep


def main():
    parser = argparse.ArgumentParser(description="A script to automatically send documents from a specified directory to a Telegram chat at a given frequency.")
    parser.add_argument('--publication_frequency', type=int, help='Publication frequency in hours (default: 4)', default=4)
    args = parser.parse_args()
    time_publication = args.publication_frequency * 3600
    token = os.environ.get('TELEGRAM_TOKEN')
    bot = telegram.Bot(token)
    chat_id = '-1002280010724'
    file_names = [f for f in os.listdir('images/') if os.path.isfile(os.path.join('images/', f))]
    random.shuffle(file_names)

    for file_name in file_names:
        file_path = os.path.join('images/', file_name)
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
        sleep(time_publication)


if __name__ == "__main__":
    main()
