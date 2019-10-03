from django.urls import NoReverseMatch

from . import schema


def reverse(feature_name, **kwargs):
    feature_schema = schema.get_schema()
    try:
        feature = feature_schema[feature_name]
    except KeyError:
        raise NoReverseMatch(feature_name)
    else:
        return feature['coerced_url'].format(**kwargs)
        

__all__ = (
    'reverse',    
)
