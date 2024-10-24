import os


import random


import telegram


import argparse


from dotenv import load_dotenv


from time import sleep


load_dotenv()

token = os.environ.get('token')
bot = telegram.Bot(token)
chat_id = '-1002280010724'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publication_frequency', type=int, help='publication frequency in hours', default=4)
    args = parser.parse_args()
    time_publication = args.publication_frequency * 3600

    file_list = [f for f in os.listdir('images/') if os.path.isfile(os.path.join('images/', f))]
    random.shuffle(file_list)

    for file_name in file_list:
        file_path = os.path.join('images/', file_name)
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
        sleep(time_publication)

if __name__ == "__main__":
    main()