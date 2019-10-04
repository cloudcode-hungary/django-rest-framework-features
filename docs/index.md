<div class="badges">
    <a href="http://travis-ci.org/balintb/cloudcode-hungary/django-rest-framework-features">
        <img src="https://travis-ci.org/balintb/cloudcode-hungary/django-rest-framework-features.svg?branch=master">
    </a>
    <a href="https://pypi.python.org/pypi/djangorestframework-features">
        <img src="https://img.shields.io/pypi/v/djangorestframework-features.svg">
    </a>
</div>

---

# Djang REST framework features

Rapid schema generation, permission management based on named features

---

## Overview

Rapid schema generation, unit generation, permission management based on named features

## Requirements

* Python (3.6)
* Django (2.2.6)
* djangorestframework (3.10.3)

## Installation

Install using `pip`...

```bash
$ pip install pip install git+ssh://git@dev.cloudcode.hu/common/django-rest-framework-features.git
```

Add `'rest_framework_features'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = [
        ...
        'rest_framework_features',
    ]

## Example

Let's take a look at a quick example of using REST framework features 
to build a simple model-backed API with named endpoints.


See the following views:

```python
from django.urls import path, include
from rest_framework import generics
from rest_framework_features import schema

@schema.view(get='listTests')
class TestListView(generics.ListAPIView):
    ...


@schema.view(get='getTest', put='updateTest', delete='deleteTest')
class TestInstanceView(generics.RetrieveUpdateDestroyAPIView):
    ...

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('test/', include([
                path('', TestListView.as_view()),
                path('<int:pk>/', TestInstanceView.as_view()),
            ])),
        ])),
    ])),
]
```

We'd also like to configure a couple of settings for our API.

Add the following to your `settings.py` module:

```python
INSTALLED_APPS = [
    ...  # Make sure to include the default installed apps here.
    'rest_framework_features',
]

REST_FRAMEWORK_FEATURES = {
    # See the docs for more information
    ...
}
```

That's it, we're done!

```bash
python manage.py features --json > src/Services/api.schema.json
```
The cli utility will print the json schema of your api which you can use in your frontend application.

The example output would be:
```json
{
  "listTests": {
    "url": "/api/v1/test/",
    "method": "get"
  },
  "getTest": {
    "url": "/api/v1/test/{id}/",
    "method": "get"
  },
  "updateTest": {
    "url": "/api/v1/test/{id}/",
    "method": "put"
  },
  "deleteTest": {
    "url": "/api/v1/test/{id}/",
    "method": "delete"
  }
}
```

You can use this export to build a named API functions, and do not care with the urls or http method names on the frontend.
Example API implementation with [axios](https://github.com/axios/axios):

```js
import axios from 'axios';
import Cookies from 'js-cookie';

import schema from './api.schema.json';

function getCSRFToken() {
  // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
  return Cookies.get('csrftoken');
}

// create axios instance with custom config, or use default
const axiosApi = axios.create({
  withCredentials: true,
  headers: {
    'X-CSRFToken': getCSRFToken(),
  },
});

// helper method to substitute coerced url parameters
// e.g. url=/api/1/getTest/{id}/, kwargs={id: 1} => /api/1/getTest/1/
function createUrlFromKwargs(url, kwargs) {
  return Object.entries(kwargs)
    .reduce(
      (result, [key, value]) => result.replace(`{${key}}`, value),
      url,
    );
}

// create an object from the schema, whose attributes are the feature names
// these attributes are functions, which will call the endpoint
// through the pre-filled url and http method.
// NOTE an extra config argument { kwargs: Object } can be used to substitute url parameters not in query string
// e.g. await api.getTest({ kwargs: { id: 1 }});
// e.g. await api.listTests();
const api = Object.entries(schema).reduce(
  (acc, [feature, {method, url}]) => (
    ({kwargs = {}, ...config}) => axiosApi({
      url: createUrlFromKwargs(url, kwargs),
      method,
      ...config,
    })
  ),
  {},
);

export default api;
```

# Documentation & Support

Full documentation for the project is available at [docs](https://www.rest-framework-features.cloudcode.hu/).

For questions and support, make submit an issue, and we will respond as soon as possible.

## Testing

Install testing requirements.

```bash
$ pip install -r requirements.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```
