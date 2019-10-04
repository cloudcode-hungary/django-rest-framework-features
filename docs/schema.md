# Schema

## view

The most important entry point for rest-framework-features.

Example usage:
```python
from rest_framework import generics
from rest_framework_features import schema

@schema.view(get='listTests')
class TestListView(generics.ListAPIView):
    ...
```


### `def view(*groups, **features):`   
This method will decorate the rest framework api views with extra information to generate the schema 
and manage permissions.

#### `*groups`
Used to define a tree of features. This is useful when used in combination with the permissions module. 
To find out more read more about permissions [here.](permissions.md)

#### `**features`
The keys must be a subset of the available http verbs 
(`get`, `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`).
The names provided must be unique overall your application. These names will be used for resolving features.