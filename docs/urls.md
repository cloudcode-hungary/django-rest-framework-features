# URLs

## reverse

Utility function for reversing urls based on the feature name, instead of the django url name.

Example usage:
```python
from rest_framework_features.urls import reverse

reverse('listTests', id=1) # /api/1/test/
reverse('getTest', id=1) # /api/1/test/1/
```

### `def reverse(feature_name, **kwargs):`   
Will find the feature in the schema, and substitute kwargs in the coerced url.

#### `feature_name`
Simply the name of the feature defined in the `view` decorator.

#### `**kwargs`
The coerced url arguments for your endpoint. 
Coercing is done by `rest_framework.schemas.generators.BaseSchemaGenerator.coerce_path`
