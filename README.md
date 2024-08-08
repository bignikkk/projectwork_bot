# Telegram bot PROJECTWORK_BOT

"Projectwork_bot" - это telegram-бот, реализованный на Python с использованием библиотеки Python-telegram-bot. Когда студент Яндекс Практикум отправляет свой проект на ревью он может запустить бота для получения уведомлений обо всех изменениях статуса проверки (ревью кода) его работы из API Яндекс.Практикум

### Автор:

Автор: Nikita Blokhin
GitHub: github.com/bignikkk

### Технологии:

Python
Python-telegram-bot
API

### Как ознакомться с проектом:

```
git clone https://github.com/bignikkk/projectwork_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создайте файл .env в корневом каталоге и добавьте свои токены:

```
PRACTICUM_TOKEN=ваш_токен_YP
TELEGRAM_BOT_TOKEN=токен_вашего_ТГ_бота
TELEGRAM_CHAT_ID=id_вашего_аккаунта
```

Запустите бота:

```
python homework.py
```