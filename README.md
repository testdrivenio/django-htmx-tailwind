# Rapid Prototyping with Django, htmx, and Tailwind CSS

### Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/django-htmx-tailwind/).

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv && source venv/bin/activate
    ```

1. Install the Python dependencies:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

1. Install the Node dependencies:

    ```sh
    $ npm install tailwindcss postcss postcss-cli autoprefixer @fullhuman/postcss-purgecss
    # you may need to install PostCSS globally as well
    # npm install --global postcss postcss-cli
    ```

1. Apply the migrations and run the Django development server:

    ```sh
    (venv)$ python manage.py migrate
    (venv)$ python manage.py runserver
    ```

1. Test at [http://localhost:8000/](http://localhost:8000/)
