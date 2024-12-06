from synapse_sdk.clients.base import BaseClient
from synapse_sdk.clients.utils import get_default_url_conversion


class MLClientMixin(BaseClient):
    def get_model(self, pk, params=None, url_conversion=None):
        path = f'models/{pk}/'
        url_conversion = get_default_url_conversion(
            url_conversion, files_fields=['files', 'parent.files'], is_list=False
        )
        return self._get(path, params=params, url_conversion=url_conversion)

    def create_model(self, data):
        path = 'models/'
        return self._post(path, data=data)

    def update_model(self, pk, data, files=None):
        path = f'models/{pk}/'
        return self._patch(path, data=data, files=files)

    def list_train_dataset(self, params=None, url_conversion=None, list_all=False):
        path = 'train_dataset/'
        url_conversion = get_default_url_conversion(url_conversion, files_fields=['files'])
        return self._list(path, params=params, url_conversion=url_conversion, list_all=list_all)
