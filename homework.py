import os
import time
import logging

import requests
from telegram import Bot
from telegram.error import TelegramError

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN_TG')
PRACTICUM_TOKEN = os.getenv('TOKEN_YA')
TELEGRAM_CHAT_ID = os.getenv('TOKEN_CHAT')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.DEBUG
)


def check_tokens():
    """Проверка доступности переменных окружения."""
    required_tokens = (ENDPOINT, TELEGRAM_TOKEN, PRACTICUM_TOKEN)
    for token_value in required_tokens:
        if not token_value:
            logging.critical(
                f'Отсутствует переменная окружения: {token_value}')
            raise RuntimeError(
                'К сожалению, отсутствует доступ к необходимому токену.'
            )


def send_message(bot, message):
    """Отправка сообщений."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug(f'Бот отправил сообщение: {message}. ')
    except TelegramError as error:
        logging.error(f'Ошибка при отправке сообщения: {str(error)}')


def get_api_answer(timestamp):
    """Отправка GET-запроса и получение ответа от API."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.RequestException as error:
        logging.error(f'Ошибка при запросе к API: {str(error)}')
    if response.status_code != 200:
        error_msg = (f'Ошибка при запросе к API: {response.status_code}.')
        logging.error(error_msg)
        raise requests.HTTPError(error_msg)

    return response.json()


def check_response(response):
    """Проверка ответа от API на соответствие ожидаемой информации."""
    if not isinstance(response, dict):
        raise TypeError('К сожалению, API вернул некорректный тип данных.')

    if 'homeworks' not in response:
        raise KeyError('К сожалению,в ответе API'
                       'отсутствует необходимый ключ.')

    if not isinstance(response['homeworks'], list):
        raise TypeError(
            'К сожалению, API вернул некорректный тип данных.')

    if 'current_date' not in response:
        raise KeyError('К сожалению,в ответе API'
                       'отсутствует необходимый ключ.')

    return True


def parse_status(homework):
    """Проверка статуса домашней работы."""
    homework_name = homework.get('homework_name')
    status = homework.get('status')

    if 'homework_name' not in homework:
        raise KeyError('К сожалению, данные о работе сейчас не доступны.')

    if status is None:
        raise KeyError('К сожалению, статус работы сейчас не доступен.')

    if status not in HOMEWORK_VERDICTS:
        raise ValueError(
            f'Недокументированный статус работы "{homework_name}": {status}')

    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()

    bot = Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:

        try:
            response = get_api_answer(timestamp)

            if check_response(response):
                for homework in response['homeworks']:
                    status_message = parse_status(homework)
                    send_message(bot, status_message)
            else:
                logging.debug('Нет новых обновлений по домашним работам')

        except Exception as error:
            logging.error(f'Сбой в работе программы: {error}')

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
