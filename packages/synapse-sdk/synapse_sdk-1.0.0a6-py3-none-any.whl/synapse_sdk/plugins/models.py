import os
from functools import cached_property
from typing import Dict, Any

from synapse_sdk.plugins.utils import read_plugin_config
from synapse_sdk.utils.storage import get_storage
from synapse_sdk.utils.string import hash_text


class PluginRelease:
    config: Dict[str, Any]

    def __init__(self, config=None, plugin_path=None):
        if config:
            self.config = config
        else:
            self.config = read_plugin_config(plugin_path=plugin_path)

    @cached_property
    def plugin(self):
        return self.config['code']

    @cached_property
    def version(self):
        return self.config['version']

    @cached_property
    def code(self):
        return f'{self.plugin}@{self.version}'

    @cached_property
    def category(self):
        return self.config['category']

    @cached_property
    def name(self):
        return self.config['name']

    @cached_property
    def checksum(self):
        return hash_text(self.code)

    @cached_property
    def actions(self):
        return list(self.config['actions'].keys())

    def setup_runtime_env(self):
        # TODO ray에 해당 plugin release runtime env 캐싱
        pass

    def get_action_config(self, action):
        return self.config['actions'][action]

    def get_url(self, storage_url):
        storage = get_storage(storage_url)
        return storage.get_url(f'{self.checksum}.zip')

    def get_serve_url(self, serve_address, path):
        return os.path.join(serve_address, self.checksum, path)


class Job:
    job_id = None

    def __init__(self, job_id):
        self.job_id = job_id
