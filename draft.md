# Rapid Prototyping with Django, htmx, and Tailwind CSS

In this tutorial, you'll learn how to set up Django with [htmx](https://htmx.org/) and [Tailwind CSS](https://tailwindcss.com/). The goal of both htmx and Tailwind is to simplify modern web development so you can design and enable interactivity without ever leaving the comfort and ease of HTML. We'll also look at how to use [Django-Compressor](https://django-compressor.readthedocs.io/en/stable/) to bundle and minify static assets in a Django app.

## htmx

[htmx](https://htmx.org/) is a library that allows you to access modern browser features like AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly from HTML, rather than using JavaScript. It allows you to build user interfaces quickly with hypertext.

htmx extends several features already built into the browser, like making HTTP requests and responding to events. For example, rather than only being able to make GET and POST requests via `a` and `form` elements, you can use HTML attributes to send GET, POST, PUT, PATCH, or DELETE requests on any HTML element:

```html
<button hx-delete="/user/1">Delete</button>
```

You can also update parts of a page to create a Single-page Application (SPA):

```
<p class="codepen" data-height="265" data-theme-id="light" data-default-tab="html,result" data-user="mjhea0" data-slug-hash="RwoJYyx" style="height: 265px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;" data-pen-title="RwoJYyx">
  <span>See the Pen <a href="https://codepen.io/mjhea0/pen/RwoJYyx">
  RwoJYyx</a> by Michael Herman (<a href="https://codepen.io/mjhea0">@mjhea0</a>)
  on <a href="https://codepen.io">CodePen</a>.</span>
</p>
<script async src="https://cpwebassets.codepen.io/assets/embed/ei.js"></script>
```

Watch the `network tab`. When the button is clicked, an XHR request is sent to the `https://v2.jokeapi.dev/joke/Any?format=txt&safe-mode` endpoint. The request's response is then appended to the `p` with an `id` of `output.

> For more examples, check out the [UI Examples](https://htmx.org/examples/) page from the official htmx docs.

### Pros and Cons

**Pros**:

1. No need to write Javascript.
1. Frameworks like Django, Ruby on rails can be fully leveraged.

**Cons**:

- Library Maturity. Since the library is quite new, documentation and example implementations are not enough for reference.
- Size of data transferred. Typically, SPA frameworks (like React and Vue) work by passing data back and forth between the client and server in JSON format. The data received is then rendered by the client. htmx, on the other hand, receives the rendered HTML from the server, and it replaces the target element with the response. The HTML in rendered format is typically larger in terms of size than a JSON response.

## Tailwind CSS

[Tailwind CSS](https://tailwindcss.com/) is a "utility-first" CSS framework. Rather than shipping pre-build components (like [Bootstrap](https://getbootstrap.com/) or [Bulma](https://bulma.io/)), it provides many building blocks (utility classes) that enable one to create layouts and designs easily and quickly.

For example, take the following HTML and CSS:

```html
<style>
.hello {
  height: 5px;
  width: 10px;
  background: gray;
  border-width: 1px;
  border-radius: 3px;
  padding: 5px;
}
</style>

<div class="hello">Hello World</div>
```

This can be implemented with Tailwind like so:

```html
<div class="h-1 w-2 bg-gray-600 border rounded-sm p-1">Hello World</div>
```

Check out the [CSS Tailwind Converter](https://tailwind-converter.netlify.app/) to convert CSS to Tailwind. Compare the results.

### Pros and Cons

**Pros**:

- Highly customizable. Although Tailwind comes with pre-built classes, they can be overwritten using the *tailwind.config.js* file.
- Optimization. PurgeCSS can remove all the unused CSS classes from the Tailwind CSS file, reducing the size of the CSS bundle.
- Dark mode. It's effortless to implement dark mode: `<div class="bg-white dark:bg-black">`

**Pros**:

- Tailwind does not provide any official prebuilt components like buttons, cards, nav bars, an so forth. Components have to be created from scratch. There are a few community-driven resources for components like [Tailwind CSS Components](https://tailwindcomponents.com/) and [Tailwind Toolbox](https://www.tailwindtoolbox.com/), to name a few.
- CSS is inline. This couples content and design, which increases the page size and clutters the HTML.

## Flask-Assets

[Django-Compressor](https://django-compressor.readthedocs.io/en/stable/) is an extension designed for managing(compressing/caching) static assets in a Django application. With it, you create a simple asset pipeline for:

1. Compiling [Sass](https://sass-lang.com/) and [LESS](http://lesscss.org/) to CSS stylesheets
1. Combining and minifying multiple CSS and JavaScript files down to a single file for each
1. Creating asset bundles for use in your templates

With that, let's look at how to work with each of the above projects in Django!

## Project Setup

To start, create a new directory for our project, create and activate a new virtual environment, and install Django along with Django-Compressor:

```bash
$ mkdir django-htmx-tailwind && cd django-htmx-tailwind
$ python3.9 -m venv venv
$ source .venv/bin/activate
(venv)$

(venv)$ pip install Django==3.1.7 django-compressor==2.4
```

Next, let's install Tailwind CSS, [PostCSS]([PostCSS](https://github.com/postcss/postcss)), [Autoprefixer](https://github.com/postcss/autoprefixer), and [PurgeCSS](https://purgecss.com/) with [NPM](https://www.npmjs.com/):

```bash
$ npm install tailwindcss postcss postcss-cli autoprefixer @fullhuman/postcss-purgecss
```

Additional tools:

- PostCSS - a tool used by Tailwind for preprocessing CSS
- Autoprefixer - a PostCSS plugin that automatically transforms CSS to support different browsers
- PurgeCSS - removes unused CSS

Next, create a new django-project and a `todos` app.

```bash
# django-htmx-tailwind

(venv)$ django-admin startproject config .
(venv)$ python manage.py startproject todos 
```

Once the `todos` app is created, add todos and the newly installed `compressor` app to our `INSTALLED_APPS`.

```python
# config/settings.py

INSTALLED_APPS = [
    ...
    "django.contrib.staticfiles",
    "todos", # new
    "compressor", # new
    ...
]
```

All our templates will be in the `templates` directory at the root of our project, configure the same in settings.py

```python
# config/settings.py

TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR / "templates"], # new
        ...
    },
]
```

Next, we need to create a new filter for our django-compressor to work with postcss. Add the following to `todos/admin.py`

```python
# todos/admin.py

from compressor.filters import CompilerFilter


class PostCSSFilter(CompilerFilter):
    command = "postcss"
```

We just created a new filter with the command to run as `postcss`. The input and output locations will be detected automatically.

For the above created filter to work, we need to add some configuration to the `config/settings.py`

```python
# config/settings.py

COMPRESS_CSS_FILTERS = ("todos.admin.PostCSSFilter",)

COMPRESS_ROOT = BASE_DIR / "static"

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)
```

1. `COMPRESS_CSS_FILTERS` define which filter to use for compressing our static assets. In our case, we'll use the on defined above.
1. `COMPRESS_ROOT` defines the absolute location from where the files to be compressed are read from and the compressed files are written to.
1. `COMPRESS_ENABLED` makes the compression work. It defaults to the opposite of DEBUG(that's why explicitly set to True).
1. `STATICFILES_FINDERS` is required if `django.contrib.staticfiles` is in INSTALLED_APPS.


We have setup django-compressor filter to run the `postcss` command. . Behind the scenes, PostCSS runs like so using a Python subprocess:

```bash
$ postcss {infile} -o {outfile}
```

where the infile will be resolved from the template `compress` tag and the outfile will be set to default(CACHE directory) by django.

> Since all Django static files reside in the "static" folder by default, the above-mentioned "infile" and "outfile" reside in the "static" folder.

With that, let's set up Tailwind and PostCSS.

Start by creating a Tailwind config file:

```bash
$ npx tailwind init
```

This should generate a *tailwind.config.js* file. All Tailwind customizations go into this file.

Next, add a *postcss.config.js* file:

```javascript
const path = require('path');

module.exports = (ctx) => ({
  plugins: [
    require('tailwindcss')(path.resolve(__dirname, 'tailwind.config.js')),
    require('autoprefixer'),
    process.env.DJANGO_PROD === 'production' && require('@fullhuman/postcss-purgecss')({
      content: [
        path.resolve(__dirname, 'templates/**/*.html')
      ],
      defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
    })
  ],
});
```

Add the following to the *static/src/main.css*:

```css
/* static/src/main.css */

@tailwind base;
@tailwind components;
@tailwind utilities;
```

Here, we defined all the `base`, `components`, and `utilities` classes from Tailwind CSS. PostCSS will build all the classes into the target location. 

> If you get a `Program file not found: postcss`, try installing PostCSS globally: `npm install --global postcss postcss-cli`.

Now that you've seen how to set up Django-compressor and tailwind, let's look at how to serve up an *index.html* file to see the CSS in action.

## Simple Example

Update the *app.py* file like so:

```python
# todos/views.py

from django.shortcuts import render


def index(request):
    return render(request, "index.html")
```

Add the view to `todos/urls.py`

```python
# todos/urls.py

from django.urls import path

from .views import index

urlpatterns = [
    path("", index, name="index"),
]
```

Finally add `todos.urls` to `config/urls.py`

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todos.urls")), # new
]
```

Create a "templates" folder. Then, add a *base.html* file to it:

```html
<!-- templates/base.html -->

{% load compress %}
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django + HTMX + TailwindCSS</title>


        {% compress css %}
        <link rel="stylesheet" href="{% static 'src/main.css' %}">
        {% endcompress %}
        <!-- <link rel="stylesheet" href="{% static 'dist/main.css' %}"> -->

    </head>
    <body class="bg-blue-100">
        {% block content %}
        {% endblock content %}
    </body>
</html>
```

1. `{% load compress %}` will import all the required tags to work with django-compressor
1. `{% load static %}` will allow us to load static files into template(`static/src/main.css`)

Take note of the `{% compress css %` block. Django will take the source file within the `compress` tag and apply filters. The `css` in compress tag tells django to apply any/all available CSS filters, recall the `COMPRESS_CSS_FILTERS` in `settings.py`.

Also, we added some color to the HTML body via `<body class="bg-blue-100">`. `bg-blue-100` is used to change the [background color](https://tailwindcss.com/docs/background-color) to light blue.

Add the *index.html* file:


```html
<!-- templates/index.html -->

{% extends "base.html" %}

{% block content %}
<h1>Hello World</h1>
{% endblock content %}
```

Start the server via `python manage.py runserver` and navigate to [http://localhost:8000](http://localhost:8000) in your browser to see the results. Also take note of the new file created under `static/CACHE/css` directory. 

With Tailwind configured, let's add htmx into the mix and build a live search that displays results as you type.

## Live Search Example

Rather than fetching the htmx library from a CDN, let's download it and use Django-Compressor to bundle it.

Download the library from [https://unpkg.com/htmx.org@1.2.1/dist/htmx.js](https://unpkg.com/htmx.org@1.2.1/dist/htmx.js) and save it to "static/src/main.js".

Navigate to [https://jsonplaceholder.typicode.com/todos](https://jsonplaceholder.typicode.com/todos) and save all the TODOs to a new file called *todos/todo.py*.

Let us now add the view to implement the search functinality.

```python
# todos/views.py

from django.views.decorators.http import require_http_methods

from .todo import todos


def index(request):
    return render(request, "index.html", {"todos": []}) # modified

# new
@require_http_methods(["POST"])
def search(request):
    res_todos = []
    search = request.POST["search"]
    if len(search) == 0:
        return render(request, "todo.html", {"todos": []})
    for i in todos:
        if search in i["title"]:
            res_todos.append(i)
    return render(request, "todo.html", {"todos": res_todos})
```

We added a new view, `search`, that can be served via POST request only and searches the todos. Now add the newly created view to `todos/urls.py`

```python
# todos/urls.py
...
from .views import index, search # modified

urlpatterns = [
    path("", index, name="index"),
    path("search/", search, name="search"), # new
]
```

Now we add the new htmx to our *base.html* file:

```html
<!-- templates/base.html -->

{% load compress %}
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django + HTMX + TailwindCSS</title>


        {% compress css %}
        <link rel="stylesheet" href="{% static 'src/main.css' %}">
        {% endcompress %}
        <!-- <link rel="stylesheet" href="{% static 'dist/main.css' %}"> -->

    </head>
    <body class="bg-blue-100">
        {% block content %}
        {% endblock content %}
        {% compress js %}
        <script type="text/javascript" src="{% static 'src/main.js' %}"></script>
        {% endcompress %}
        <script>
            document.body.addEventListener('htmx:configRequest', (event) => {
                event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
            })
        </script>
    </body>
</html>
```

We load the htmx library using the `compress js` tag. This will bundle the js file and serve it from `static/CACHE` directory.

We also added the following script to our base html

```js
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})
```

Whenever there is a request from htmx, the script automatically adds the `csrf_token` to the request headers.

We'll add the ability to search based on the title of each todo.

Add the following to the `index.html` file.

```html
<!-- templates/index.html -->
{% extends 'base.html' %}

{% block content %}
<div class="w-small w-2/3 mx-auto py-10 text-gray-600">

    <input type="text" name="search" hx-post="/search/" hx-trigger="keyup changed delay:250ms"
        hx-indicator=".htmx-indicator" hx-target="#todo-results" placeholder="Search"
        class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none">
    <span class="htmx-indicator">
        Searching...
    </span>
</div>
<table class="border-collapse w-small w-2/3 mx-auto">
    <thead>
        <tr>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                #</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                Title</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                Completed</th>
        </tr>
    </thead>
    <tbody id="todo-results">
        {% include 'todo.html' %}
    </tbody>
</table>
{% endblock content %}
```

Let's take a moment to look at the attributes defined from htmx:

```html
<input
  type="text"
  name="search"
  hx-post="/search"
  hx-trigger="keyup changed delay:250ms"
  hx-indicator=".htmx-indicator"
  hx-target="#todo-results"
  placeholder="Search"
  class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none"
>
```

1. The input sends a POST request to the `/search` endpoint.
1. The request is triggered via the keyup event with a delay of 250ms. So if a new keyup event is entered before 250ms elapses between the last keyup, the request is not triggered.
1. The HTML response from the request is then displayed in the `#todo-results` element.
1. We also have an indicator, a loading element that appears after the request is sent and disappears after the response comes back.

Add the *templates/todo.html* file:

```html
<!-- templates/todo.html -->

{% for todo in todos %}
<tr
    class="bg-white lg:hover:bg-gray-100 flex lg:table-row flex-row lg:flex-row flex-wrap lg:flex-no-wrap mb-10 lg:mb-0">
    <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {{todo.id}}
    </td>
    <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {{todo.title}}
    </td>
    <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {% if todo.completed %}
        <span class="rounded bg-green-400 py-1 px-3 text-xs font-bold">Yes</span>
        {% else %}
        <span class="rounded bg-red-400 py-1 px-3 text-xs font-bold">No</span>
        {% endif %}

    </td>
</tr>
{% empty %}
{% endfor %}
```

This file renders the TODOs that match our search query. The `/search` endpoint searches for the TODOs and renders the *todo.html* template with all the results.


Run the application using `python manage.py runserver` and navigate to [http://localhost:8000](http://localhost:8000) again to test it out

# Demo here

## Removing unwanted CSS

The size of the *static/dist/main.css* is roughly 3.9MB because we generated the whole Tailwind CSS file. That said, since we are only using a few classes for styling, we can remove unused CSS via [PurgeCSS](https://purgecss.com/).

We already configured it earlier in *postcss.config.js*:

```javascript
process.env.DJANGO_PROD === 'production' && require('@fullhuman/postcss-purgecss')({
  content: [
    path.resolve(__dirname, 'templates/**/*.html')
  ],
  defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
})
```

So, when `DJANGO_PROD` is 'production', PurgeCSS wil walk through all the HTML files in the templates directory and remove unused CSS.

To test, fist set the environment variable:

```bash
(venv)$ export DJANGO_PROD=production # for Linux

(venv)$ set DJANGO_PROD=production # for windows
```

Start the app and inspect the newly created *static/dist/main.css* file. It should now only be 12KB! Nice. Ensure the app still works before moving on.

## Conclusion

In this tutorial, we looked at how to:

- Set up Django-Compressor and Tailwind CSS
- Build a live search app using Django, TailwindCSS, and htmx
- Remove unused CSS with PurgeCSS

htmx can render elements without reloading the page. Although this reduces the amount of work done on the client-side, the data sent from the server can be higher since it's sending rendered HTML. The library is still young, but the future looks bright for it.


Html + websockets is gaining popularity. This approach delivers realtime changes(html) to the webpage using websockets instead of using a javascript framework. The same approach is used by the famous [Phoenix LiveView](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html). Read more about html over websockets in the article "[The Future of Web Software Is HTML-over-WebSockets](https://alistapart.com/article/the-future-of-web-software-is-html-over-websockets/)"    

Tailwind is a powerful CSS framework that focuses on developer productivity. It's highly customizable.

Here are some resources for tailwind customization

- [TailwindCSS Customization](https://tailwindcss.com/docs/configuration)
- [The complete guide to customizing a Tailwind CSS theme](https://pinegrow.com/tutorials/customizing-a-tailwind-css-theme/)
- [Customize the Tailwind Design System](https://egghead.io/lessons/tailwind-customize-the-tailwind-design-system)
- [A gentle guide to customization in TailwindCSS](https://dev.to/developeraspire/a-gentle-guide-to-customization-in-tailwindcss-9cp)
