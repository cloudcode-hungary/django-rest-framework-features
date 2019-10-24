django-rest-framework-features
======================================

.. image:: https://readthedocs.org/projects/django-rest-framework-features/badge/?version=latest
    :target: https://django-rest-framework-features.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/cloudcode-hungary/django-rest-framework-features.svg?branch=master
    :target: https://travis-ci.org/cloudcode-hungary/django-rest-framework-features.svg?branch=master
    :alt: Build Status
.. image:: https://badge.fury.io/py/djangorestframework-features.svg
    :target: https://badge.fury.io/py/djangorestframework-features

Overview
--------

Advanced schema generation based on named features

Requirements
------------

-  Python (3.6)
-  Django (2.2.6)
-  Django REST Framework (3.10.3)

Installation
------------

Install using pip

.. code:: bash

    $ pip install djangorestframework-features

Add 'rest_framework_features' to your INSTALLED_APPS setting.

.. code:: python

   INSTALLED_APPS = [
       ...
       'rest_framework_features',
   ]

Example
-------

Let’s take a look at a quick example of using REST framework features to
build a simple model-backed API with named endpoints.

See the following views:

.. code:: python

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

We’d also like to configure a couple of settings for our API.

Add the following to your settings.py module:

.. code:: python

   INSTALLED_APPS = [
       ...  # Make sure to include the default installed apps here.
       'rest_framework_features',
   ]

   REST_FRAMEWORK_FEATURES = {
       # See the docs for more information
       ...
   }

That’s it, we’re done!

.. code:: bash

   python manage.py features --json > src/Services/api.schema.json

The cli utility will print the json schema of your api which you can use
in your frontend application.

The example output would be:

.. code:: json

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

You can use this export to build a named API functions, and do not care
with the urls or http method names on the frontend. Example API
implementation with `axios`:

.. code:: javascript

    import axios from 'axios';
    import Cookies from 'js-cookie';

    import schema from './api.schema.json';

    function getCSRFToken() {
        // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
        return Cookies.get('csrftoken');
    }

    // create axios instance with custom config, or use default const
    axiosApi = axios.create({
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


Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent tox testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you'll need to install mkdocs.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build
