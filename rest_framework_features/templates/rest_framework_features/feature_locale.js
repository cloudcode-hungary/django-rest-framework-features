(function () {
  return {
{% for feature_name, feature_def in schema.items %}    {{ feature_name }}: window.django.pgettext('api', '{{ feature_def.verbose_name }}'),
{% endfor %}  }
})
