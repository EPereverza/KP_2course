## Тема 3
### GET и POST запросы в CLI с помощью Telnet

```
Утилиты CLI
telnet:
Windows — может понадобиться включить компонент
Debian — apt install telnet
netcat:
Windows и дистрибутивы Linux — https://serverspace.ru/support/help/kak-ustanovit-netcat-na-windows-i-linux/
Debian — apt install netcat-traditional
curl — https://curl.se/docs/manpage.html
HTTPie — https://httpie.io/docs/cli
Утилиты GUI
Insomnia — https://insomnia.rest/
Postman — https://www.postman.com/
HTTPie — https://httpie.io/docs/desktop
Теоретические материалы
Ультимативный гайд по HTTP. Структура запроса и ответа
Кодирование URL — https://en.wikipedia.org/wiki/Percent-encoding
Заголовок Host — https://stackoverflow.com/questions/43156023/what-is-http-host-header
Инструменты
Кодирование и декодирование URL — https://meyerweb.com/eric/tools/dencoder/
Публичные API:
https://free-apis.github.io/
https://github.com/public-apis/public-apis
```
### Практическая работа 
```
Изучите материалы по ссылкам, которые размещены в теме.
Отправьте GET и POST запросы на любой веб-ресурс (см. публичные API в материалах темы) в CLI с помощью Telnet или netcat.
Отправьте запросы, выполненные по заданию 2, с помощью cURL.
Установите Insomnia, Postman, HTTPie Desktop или другой инструмент. Отправьте с его помощью GET-запрос для получения курса одной выбранной валюты за выбранный период (задайте любые значения). Используйте API Банка России: https://www.cbr.ru/development/sxml/
Запустите два процесса netcat — сервер (netcat -l) и клиент (подключается к localhost). Проверьте работу полученного простейшего чата и продемонстрируйте скриншотами в отчёте.
Подготовьте отчёт, который включает описание действий и скриншоты с результатами выполнения.
```