from synapse_sdk.clients.base import BaseClient
from synapse_sdk.clients.utils import get_default_url_conversion


class AnnotationClientMixin(BaseClient):
    def get_project(self, pk):
        path = f'projects/{pk}/'
        return self._get(path)

    def get_label_tag(self, pk):
        path = f'label_tags/{pk}/'
        return self._get(path)

    def list_label_tags(self, data):
        path = 'label_tags/'
        return self._list(path, data=data)

    def list_labels(self, data, url_conversion=None, list_all=False):
        path = 'labels/'
        url_conversion = get_default_url_conversion(url_conversion, files_fields=['files'])
        return self._list(path, data=data, url_conversion=url_conversion, list_all=list_all)

    def create_labels(self, data):
        path = 'labels/'
        return self._post(path, data=data)

    def set_tags_labels(self, data, params=None):
        path = 'labels/set_tags/'
        return self._post(path, data=data, params=params)
