from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractBaseFeature(models.Model):
    class Meta:
        abstract = True
        unique_together = ('parent', 'name')
        ordering = ('hierarchical_name',)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        verbose_name=_('name'),
        max_length=64,
    )
    parent = models.ForeignKey(
        verbose_name=_('parent'),
        to='self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    hierarchical_name = models.CharField(
        verbose_name=_('name'),
        max_length=256,
    )

    def save(self, *args, **kwargs):
        if not self.hierarchical_name:
            if self.parent_id:
                self.hierarchical_name = '/'.join([self.parent.hierarchical_name, self.name])
            else:
                self.hierarchical_name = self.name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.hierarchical_name


class Feature(AbstractBaseFeature):
    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


__all__ = (
    'AbstractBaseFeature',
    'Feature',
)
