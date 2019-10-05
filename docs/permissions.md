# Permissions

## CanAccessFeature

Rest framework permission class for handling authorization based on view feature groups.

### `CanAccessFeature(IsAuthenticated):`

Example usage:
```python
from rest_framework import generics
from rest_framework_features import schema, permissions

@schema.view('test', get='getTest')
class TestRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.CanAccessFeature,)
```
or configure with rest framework `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework_features.permissions.CanAccessFeature',
    ),
}
```

This class will check the user's permissions, looking the relevant feature tree.
Users with `is_superuser=True` are permitted regardless of their feature permissions.
In the above example, the `has_permission` method will check if the user has one of the permissions:

- `'rest_framework_features.test'`
- `'rest_framework_features.test_getTest'`

To see a more complex example:

```python
from rest_framework import generics
from rest_framework_features import schema, permissions

@schema.view('warehouse', 'stock', get=('read', 'getStock'), put=('write', 'updateStock'), delete=('write', 'deleteStock'))
class WarehouseStockInstanceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.CanAccessFeature,)
    
    
@schema.view('warehouse', 'location', get=('read', 'listLocations'))
class WarehouseLocationInstanceView(generics.ListAPIView):
    permission_classes = (permissions.CanAccessFeature,)
    
# admin can access (getStock, updateStock, deleteStock, listLocations)
admin = User.objects.create(is_superuser=True)

# manager can access (getStock, updateStock, deleteStock, listLocations)
warehouse_manager = User.objects.create()
warehouse_manager.permissions.add('rest_framework_features.warehouse')

# worker can access (getStock, updateStock, deleteStock)
warehouse_worker = User.objects.create()
warehouse_worker.permissions.add('rest_framework_features.warehouse_stock')

# supervisor can access (getStock, updateStock, listLocations)
warehouse_supervisor = User.objects.create()
warehouse_supervisor.permissions.add('rest_framework_features.warehouse_stock_read')
warehouse_supervisor.permissions.add('rest_framework_features.warehouse_stock_write_updateStock')
warehouse_supervisor.permissions.add('rest_framework_features.warehouse_location_read')
```

Lucky for your these permissions can be generated using the `ENABLE_PERMISSIONS` setting.
To read more about settings click [here.](settings.md)