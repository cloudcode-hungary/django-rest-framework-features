from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import querysets


class AbstractBaseFeature(models.Model):
    class Meta:
        abstract = True
        unique_together = ('parent', 'name')

    objects = querysets.FeatureQuerySet.as_manager()

    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    name = models.CharField(
        verbose_name=_('name'),
        max_length=50,
    )
    parent = models.ForeignKey(
        verbose_name=_('parent'),
        to='self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )

    def __str__(self):
        return getattr(self, 'display_name', self.name)


class Feature(AbstractBaseFeature):
    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


__all__ = (
    'AbstractBaseFeature',
    'Feature',
)
