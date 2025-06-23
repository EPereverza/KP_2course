### Задание
```
Создайте бота-переводчика для Telegram с использованием Cloud Functions и API Gateway.
Вы можете выбрать любые язык программирования (из поддерживаемых Yandex Cloud) и библиотеку для взаимодействия с Telegram Bot API.

Бот должен обрабатывать команды /start и /help. Любой другой ввод должен обрабатываться ботом как текст, который необходимо перевести на другой язык (любой на выбор студента).

Для перевода используйте LibreTranslate (сайт, репозиторий). Публичный сервер, для использования которого не нужен API-ключ: https://translate.flossboxin.org.in/ (см. раздел Mirrors на странице GitHub).

В ответе необходимо указать:

адрес Cloud Function и скриншот кода функции;
описание API Gateway и скриншот;
ник Telegram-бота.
```

```
curl.exe `
   --request POST `
   --url https://api.telegram.org/bot<тут токена нет>/setWebhook `
   --header '"Content-type: application/json"' `
   --data '"{ \"url\": \"https://d5dc3gvpnggqh85iks0l.trruwy79.apigw.yandexcloud.net\" }"'
```
```
curl "https://api.telegram.org/bot<нет>/getWebhookInfo"
```
