from django.db.models import QuerySet
from django.db.models.expressions import RawSQL


class FeatureQuerySet(QuerySet):
    def with_display_names(self):
        feature = self.model._meta.db_table
        return self.annotate(
            display_name=RawSQL(f'''
                with recursive 
                    {feature}_level(id, name) as (
                        select
                            {feature}.id
                            , cast({feature}.name as text)
                        from {feature}
                        where {feature}.parent_id is null
                        union all
                        select 
                            {feature}.id
                            , {feature}_level.name || '/' || {feature}.name
                        from {feature}_level
                        join {feature} on {feature}.parent_id = {feature}_level.id
                    ) 
                select {feature}_level.name
                from {feature}_level
                where {feature}_level.id = {feature}.id -- referencing outer query
                ''', (), ),
        ).order_by(
            'display_name',
        )


__all__ = (
    'FeatureQuerySet',
)
