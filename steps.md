# Django + HTMX

1. Prepare the virtual environment and create a new Django project

  ```bash
  virtualenv .venv
  source .venv/bin/activate

  pip install Django==3.1.7

  django-admin startproject config .
  python manage.py startapp todos
  ```

1. Add todos to installed apps

1. Configure templates to use `basedir/templates`

1. Add `todo.py` to todos application

1. Add views to render the template and response

1. Add urls to app urls

1. Setup tailwind and postcss configuration

1. Install django-compressor and add to apps

1. create postcss filter class in `todos/admin.py`

1. add `COMPRESS_ROOT`, `COMPRESS_ENABLED`, `COMPRESS_CSS_FILTERS` and `STATICFILES_FINDERS` to settings.py
