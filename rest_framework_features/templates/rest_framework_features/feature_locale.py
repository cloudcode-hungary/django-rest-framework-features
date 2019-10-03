from django.utils.translation import pgettext

API = {
{% for feature_name, feature_def in schema.items %}    '{{ feature_name }}': pgettext('api', '{{ feature_def.verbose_name }}'),
{% endfor %}}
