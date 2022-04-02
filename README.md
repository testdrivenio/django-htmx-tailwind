# Rapid Prototyping with Django, htmx, and Tailwind CSS

### Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/django-htmx-tailwind/).

## Want to use this project?

1. Fork/Clone

2. Create and activate a virtual environment:

    ```sh
    $ python3.10 -m venv venv && source venv/bin/activate
    ```

3. Install the Python dependencies:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

4. Install and setup Tailwind CSS:

    ```sh
    $ pip install pytailwindcss
    $ tailwindcss
    ```

5. Scan templates and generate CSS file:
    
    ```sh
    $ tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify
    ```

6. Apply the migrations and run the Django development server:

    ```sh
    (venv)$ python manage.py migrate
    (venv)$ python manage.py runserver
    ```

6. Test at [http://localhost:8000/](http://localhost:8000/)
