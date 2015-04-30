import logging
from tastypie.resources import ModelResource


class BaseResource(ModelResource):
    logger = logging.getLogger(__name__)
    pass

    def _remove_kwargs(self, *args, **kwargs):
        for arg in args:
            if arg in kwargs:
                del kwargs['activity_sharing_networks_facebook']

        return kwargs

    @staticmethod
    def hydrate_bitfield(field_name, bundle, object_field, choices, remove_field=True):
        if not hasattr(bundle, field_name + '____processed'):
            mask = 0
            for choice in choices:
                if choice[0] in bundle.data[field_name]:
                    if bundle.data[field_name][choice[0]]:
                        mask |= getattr(object_field, choice[0])

            bundle.data[field_name] = mask
            setattr(bundle, field_name + '____processed', True)
        return bundle

    @staticmethod
    def dehydrate_bitfield(field_name, bundle, object_field, choices, remove_field=True):
        if remove_field:
            del bundle.data[field_name]

        d = {}
        for choice in choices:
            d[choice[0]] = getattr(object_field, choice[0]).is_set

        bundle.data[field_name] = d
        return bundle