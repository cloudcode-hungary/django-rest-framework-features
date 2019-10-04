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


`def view(*groups, **features):`   
This method will decorate the rest framework api views with extra information to generate the schema and manage permissions.

