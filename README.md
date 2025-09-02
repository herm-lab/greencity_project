Для запуска нужно активировать frontend и backend:
    Открыть 2 окна терминала:
        -в первом*: cd backend(переход в папку backend)+enter, 
        далее прописать: python api.py + enter. В логах можно найти логины пользователей, 
        которые есть в базе(например, Y97033). Он нужен для авторизации в системе.
        -во втором: cd frontend + enter, python main.py + enter.
        Через несколько секунд откроется экран авторизации(login.py).

Также можно запустить отдельный экран(тестирование):
    1. Запустить backend(как в *)
    2. Запустить файл окна из frontend(frontend\screens). Для запуска нужно указать
    полный путь, иначе будет ошибка об отсутствии файла(
    [Errno 2] No such file or directory). Вот шаблон:
    python frontend\screens\название экрана + enter

Чтобы проект запустился должны быть установлены следующие
модули и библиотеки:
        Package            Version
------------------ --------
blinker            1.9.0
certifi            2025.8.3
charset-normalizer 3.4.2
click              8.2.1
colorama           0.4.6
docutils           0.22
filetype           1.2.0
Flask              3.1.1
Flask-Cors         3.0.10
Flask-SQLAlchemy   3.0.3
greenlet           3.2.4
idna               3.10
itsdangerous       2.2.0
Jinja2             3.1.6
Kivy               2.3.1
kivy-deps.angle    0.4.0
kivy-deps.glew     0.3.1
kivy_deps.sdl2     0.8.0
Kivy-Garden        0.1.5
MarkupSafe         3.0.2
pip                25.2
psycopg2-binary    2.9.6
Pygments           2.19.2
pypiwin32          223
python-dotenv      1.0.0
pywin32            311
requests           2.32.4
setuptools         65.5.0
six                1.17.0
SQLAlchemy         2.0.42
typing_extensions  4.14.1
urllib3            2.5.0
Werkzeug           3.1.3

Чтобы проверить наличие установленных библиотек:
    в новом терминале: pip list

-Дополнительно лучше проверить наличие venv(в терминале
до пути проекта должно быть написано зеленым (venv)). Если нет
старое окружение и поставить заново. После переустановки проверить
наличие всех библиотек: pip list
        
