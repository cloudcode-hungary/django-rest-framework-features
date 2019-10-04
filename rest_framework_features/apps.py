from django.apps import AppConfig
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from . import schema, settings, permissions


class RestFrameworkFeaturesConfig(AppConfig):
    name = 'rest_framework_features'
    verbose_name = 'Django REST framework features'

    def ready(self):
        if settings.feature_settings.ENABLE_FEATURES:
            post_migrate.connect(sync_features, sender=self)
        if settings.feature_settings.ENABLE_PERMISSIONS:
            post_migrate.connect(sync_permissions, sender=self)


def sync_features(*args, **kwargs):
    model = settings.feature_settings.DB_MODEL
    feature_schema = schema.get_schema(False)
    with transaction.atomic():
        current_features = []
        for feature_def in feature_schema.values():
            description = feature_def['description']
            parent = None
            for name in description:
                current_features.append((parent, name))
                parent, created = model.objects.get_or_create(
                    name=name,
                    parent=parent,
                )
        current_features_query = Q()
        for (parent, name) in current_features:
            current_features_query = current_features_query | Q(parent=parent, name=name)
        model.objects.exclude(current_features_query).delete()


def sync_permissions(*args, **kwargs):
    model = settings.feature_settings.DB_MODEL
    feature_schema = schema.get_schema(False)
    content_type = ContentType.objects.get_for_model(model)
    with transaction.atomic():
        current_permissions = []
        for feature_def in feature_schema.values():
            description = feature_def['description']
            for i, codename in enumerate(permissions.get_codenames_from_description(description)):
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    name=description[i],
                )
                current_permissions.append(permission.id)
        Permission.objects.filter(content_type=content_type).exclude(id__in=current_permissions).delete()


__all__ = (
    'RestFrameworkFeaturesConfig',
)
