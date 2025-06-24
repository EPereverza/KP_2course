## Тема 1
### Развертывание сайта на Hugo.

Был установлен и развернут статический сайт с помощью Hugo Framework и темы blowfish. </br>
Сгенерирован ssh ключ для работы с Git и GitHub. Создан локальный репозиторий и привязан к GitHub репозиторию. </br>
Установлена и настроена тема blowfish портфолио через submodule Git. В завершении был создан скрипт </br>
для развертывания Hugo с помощью GitHub Action.

### Ссылка на репозиторий с исходниками сайта: 

`https://github.com/EPereverza/WhoverPortfolio`

### Ссылка на развёрнутый GitHub Pages сайт с портфолио:

`https://epereverza.github.io/WhoverPortfolio/`

yml скрипт автоматически:

1. Устанавливает необходимые зависимости (Hugo, Dart Sass, Node.js пакеты).

2. Собирает сайт с использованием Hugo.

3. Загружает результат сборки в GitHub Actions.

4. Разворачивает сайт на GitHub Pages.
Ссылка на скрипт:</br>
`https://github.com/EPereverza/WhoverPortfolio/blob/master/.github/workflows/hugo.yml`