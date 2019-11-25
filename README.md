## Index

#### main.py
Основной Telegram Bot.
Ведет ```CHAT_ID``` для использования кастомного ```logging.Handler``` и сам бот принимает логи и принимает сообщения от DialogFlow (работает хорошо)

#### vk_bot.py
Бот для VK. Принимает сообщения от DialogFlow.

#### df_teacher.py
Скрипт для обучения DialogFlow новым Intent'ам из JSON-файла ```questions.json```


## Проблема
При деплое на Heroku я использовал одно приложение и два процесса перечисленных в ```Procfile```

Heroku оба процесса запускает и они работают, как два ```__main__``` файла. Оба бота работают нормально.

Но логи приходят в чат Telegram только из модуля ```main.py``` и не приходят из ```vk_bot.py```.

Точно также ```vk_bot.py``` не видит добавленных в ```main.py``` обработчиков и свойство ```vk_logger.handlers``` возвращает пустой список. Логи ведуться в консоль нормально с дефолтными настройками (т.е. ошибки выводятся в stderr), при этом с форматированнием установленным в ```main.py```.

Выглядит вот так (лог из Heroku CLI):

![Log](./images/heroku_cli_logging.png)

Буду признателен за подсказку.
