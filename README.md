This project is designed to allow employees to request time off from work

structure is
BaseDir
    app
        static
            css
        templates
            .html
        __init__.py
        models.py
        views.py
    config.py
    manage.py
    README.md

[tool.poetry]
name = "myTimeOffRequest"
version = "0.1.0"
description = ""
authors = ["SleepyLink1 <88170820+SleepyLink1@users.noreply.github.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0.1"
pre-commit = "^3.6.0"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

```
### Installation
```
    $ git clone
    $ cd into directory
    $ pip install -r requirements.txt
    $ python manage.py runserver
```
