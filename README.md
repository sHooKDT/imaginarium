# Воображариум
Web-локализация карточной игры Имаджинариум (aka Dixit)

## Технологии
Backend -> Python + Tornado
Frontend -> HTML5 + AngularJS + SCSS
Interaction -> Websocket
Build -> GruntJS

## Сборка
1. Установить __iojs__ или __Node__ (для сборки)
2. Установить __CPython__ и __Tornado__ (_pip install tornado_)
3. Установить необходимые JS модули с помощью _npm init_
4. Собрать проект командой _grunt build_
5. Сжать и скопировать в релизную папку карты командой _grunt cards_

## Игра
1. Запускаем сервер (_static-server.py_)
2. Открываем в браузере _localhost:port_ (порт будет указан в консоли)
3. Ваши друзья подключаются по вашему IP и указанному порту
4. ???
5. PROFIT!!!

## **Сделано на GoTo Camp.**