import inspect
import json
import os
from functools import cached_property
from pprint import pprint

import ray
import requests
from ray.dashboard.modules.job.sdk import JobSubmissionClient

from synapse_sdk.clients.backend import BackendClient
from synapse_sdk.loggers import ConsoleLogger, BackendLogger
from synapse_sdk.plugins.enums import RunMethod
from synapse_sdk.plugins.models import PluginRelease
from synapse_sdk.plugins.upload import build_and_upload, archive_and_upload, download_and_upload
from synapse_sdk.utils.module_loading import import_string


class Action:
    name = None
    category = None
    method = None
    params = None
    plugin_config = None
    plugin_release = None
    config = None
    client = None
    logger = None
    debug = False

    default_envs = [
        'RAY_DASHBOARD_URL',
        'RAY_SERVE_ADDRESS',
        'SYNAPSE_PLUGIN_STORAGE',
        'SYNAPSE_DEBUG_PLUGIN_PATH',
        'SYNAPSE_DEBUG_MODULES',
        'SYNAPSE_PLUGIN_RUN_HOST',
        'SYNAPSE_PLUGIN_RUN_USER_TOKEN',
        'SYNAPSE_PLUGIN_RUN_TENANT',
    ]

    def __init__(self, params, plugin_config, envs=None, job_id=None, direct=False, debug=False):
        self.params = params
        self.plugin_config = plugin_config
        self.plugin_release = PluginRelease(config=plugin_config)
        self.config = self.plugin_release.get_action_config(self.name)
        self.job_id = job_id
        self.direct = direct
        self.debug = debug
        self.envs = {**envs, **self.get_default_envs()} if envs else self.get_default_envs()
        self.set_logger()

    @cached_property
    def entrypoint(self):
        return import_string(self.config['entrypoint'])

    @property
    def plugin_storage_url(self):
        return self.envs['SYNAPSE_PLUGIN_STORAGE']

    @property
    def plugin_url(self):
        if self.debug:
            plugin_path = self.envs.get('SYNAPSE_DEBUG_PLUGIN_PATH', '.')
            if plugin_path.startswith('https://'):  # TODO ray에서 지원하는 remote uri 형식 (https, s3, gs) 모두 지원
                plugin_url = plugin_path
            elif plugin_path.startswith('http://'):
                plugin_url = download_and_upload(plugin_path, self.plugin_storage_url)
            else:
                plugin_url = archive_and_upload(plugin_path, self.plugin_storage_url)
            self.envs['SYNAPSE_DEBUG_PLUGIN_PATH'] = plugin_url
            return plugin_url
        return self.plugin_release.get_url(self.plugin_storage_url)

    @property
    def debug_modules(self):
        debug_modules = []
        for module_path in self.envs.get('SYNAPSE_DEBUG_MODULES', '').split(','):
            if module_path.startswith('https://'):  # TODO ray에서 지원하는 remote uri 형식 (https, s3, gs) 모두 지원
                module_url = module_path
            else:
                module_url = build_and_upload(module_path, self.plugin_storage_url)
            debug_modules.append(module_url)
        self.envs['SYNAPSE_DEBUG_MODULES'] = ','.join(debug_modules)
        return debug_modules

    def set_logger(self):
        if self.job_id:
            client = BackendClient(
                self.envs['SYNAPSE_PLUGIN_RUN_HOST'],
                self.envs['SYNAPSE_PLUGIN_RUN_USER_TOKEN'],
                self.envs['SYNAPSE_PLUGIN_RUN_TENANT'],
            )
            self.logger = BackendLogger(client, self.job_id)
        else:
            self.logger = ConsoleLogger()

    def get_default_envs(self):
        return {env: os.environ[env] for env in self.default_envs if env in os.environ}

    def get_runtime_env(self):
        runtime_env = {
            'pip': ['-r ${RAY_RUNTIME_ENV_CREATE_WORKING_DIR}/requirements.txt'],
            'working_dir': self.plugin_url,
        }

        if self.debug:
            runtime_env['pip'] = self.debug_modules + runtime_env['pip']

        # 맨 마지막에 진행되어야 함
        runtime_env['env_vars'] = self.envs

        if self.debug:
            pprint(runtime_env)
        return runtime_env

    def run(self):
        return self.entrypoint(self, **self.params)

    def run_action(self):
        if self.direct:
            if self.method == RunMethod.RESTAPI:
                return self.run_by_restapi()
            else:
                return self.run()
        return getattr(self, f'run_by_{self.method.value}')()

    def run_by_task(self):
        @ray.remote(runtime_env=self.get_runtime_env())
        def run_task(category, action, *args, **kwargs):
            from synapse_sdk.plugins.utils import get_action_class

            action = get_action_class(category, action)(*args, **kwargs)
            return action.run_action()

        init_signature = inspect.signature(self.__class__.__init__)

        args = []
        kwargs = {}

        for param in init_signature.parameters.values():
            if param.name == 'self':
                continue
            if param.default == param.empty:
                args.append(getattr(self, param.name))
            else:
                kwargs[param.name] = getattr(self, param.name)

        kwargs['direct'] = True
        return ray.get(run_task.remote(self.category.value, self.name, *args, **kwargs))

    def run_by_job(self):
        main_options = []
        options = ['run', '--direct']
        arguments = [self.name, f'{json.dumps(json.dumps(self.params))}']

        if self.debug:
            main_options.append('--debug')

        if self.job_id:
            options.append(f'--job-id={self.job_id}')

        cmd = ' '.join(main_options + options + arguments)

        client = JobSubmissionClient(address=self.envs.get('RAY_DASHBOARD_URL'))
        return client.submit_job(
            submission_id=self.job_id,
            entrypoint=f'python main.py {cmd}',
            runtime_env=self.get_runtime_env(),
        )

    def run_by_restapi(self):
        path = self.params.pop('path', '')
        method = self.params.pop('method')

        url = self.plugin_release.get_serve_url(self.envs['RAY_SERVE_ADDRESS'], path)
        response = getattr(requests, method)(url, **self.params)
        # TODO ok response가 아닌 경우 대응하기
        return response.json()

    def set_progress(self, current, total, category=''):
        self.logger.set_progress(current, total, category)

    def log(self, action, data):
        self.logger.log(action, data)

    def log_event(self, message):
        self.logger.log('event', {'content': message})

    def end_log(self):
        self.log_event('Plugin run is complete.')
