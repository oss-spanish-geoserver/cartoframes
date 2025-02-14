from copy import deepcopy
from warnings import warn

from carto.kuvizs import KuvizManager
from carto.exceptions import CartoException

from .source import Source
from ..columns import normalize_name


class Kuviz(object):
    PRIVACY_PUBLIC = 'public'
    PRIVACY_PASSWORD = 'password'

    def __init__(self, id, url, name, privacy=PRIVACY_PUBLIC):
        self.id = id
        self.url = url
        self.name = name
        self.privacy = privacy

    @classmethod
    def create(cls, html, name, context=None, password=None):
        from ..auth import _default_context
        carto_kuviz = _create_carto_kuviz(context=context or _default_context, html=html, name=name, password=password)
        _validate_carto_kuviz(carto_kuviz)
        return cls(carto_kuviz.id, carto_kuviz.url, carto_kuviz.name, carto_kuviz.privacy)

    @classmethod
    def all(cls, context):
        # km = KuvizManager(context.auth_client)
        # return km.all()
        pass

    def update(self, html, name, password=None):
        pass

    def delete(self):
        pass


# FIXME: https://github.com/CartoDB/carto-python/issues/122
# Remove the function and usage after the issue will be fixed
def _validate_carto_kuviz(carto_kuviz):
    if not carto_kuviz or not carto_kuviz.url or not carto_kuviz.id or not carto_kuviz.name:
        raise CartoException('Error creating Kuviz. Something goes wrong')

    if carto_kuviz.privacy and carto_kuviz.privacy not in [Kuviz.PRIVACY_PUBLIC, Kuviz.PRIVACY_PASSWORD]:
        raise CartoException('Error creating Kuviz. Invalid privacy')

    return True


def _create_carto_kuviz(context, html, name, password=None):
    km = KuvizManager(context.auth_client)
    return km.create(html=html, name=name, password=password)


class KuvizPublisher(object):
    def __init__(self, vmap, context=None):
        self._layers = deepcopy(vmap.layers)
        self._context = context

    def set_context(self, context=None):
        from ..auth import _default_context
        self._context = context or _default_context

    def publish(self, html, name, password=None):
        return Kuviz.create(context=self._context, html=html, name=name, password=password)

    def is_sync(self):
        return all(layer.source.dataset.is_saved_in_carto for layer in self._layers)

    def get_layers(self, maps_api_key='default_public'):
        for layer in self._layers:
            layer.source.dataset.context = self._context

            layer.source.credentials = {
                'username': self._context.creds.username(),
                'api_key': maps_api_key,
                'base_url': self._context.creds.base_url()
            }

        return self._layers

    def sync_layers(self, table_name, context=None):
        for idx, layer in enumerate(self._layers):
            table_name = normalize_name("{name}_{idx}".format(name=table_name, idx=idx + 1))

            from ..auth import _default_context
            dataset_context = context or layer.source.dataset.context or _default_context

            self._sync_layer(layer, table_name, dataset_context)

    def _sync_layer(self, layer, table_name, context):
        if not layer.source.dataset.is_saved_in_carto:
            layer.source.dataset.upload(table_name=table_name, context=context)
            layer.source = Source(table_name, context=context)
            warn('Table `{}` created. In order to publish the map, you will need to create a new Regular API '
                 'key with permissions to Maps API and the table `{}`. You can do it from your CARTO dashboard or '
                 'using the Auth API. You can get more info at '
                 'https://carto.com/developers/auth-api/guides/types-of-API-Keys/'.format(table_name, table_name))
