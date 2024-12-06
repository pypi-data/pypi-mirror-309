from synapse_sdk.clients.base import BaseClient


class ServiceClientMixin(BaseClient):
    def run_plugin_release(self, code, data):
        path = f'plugin_releases/{code}/run/'
        return self._post(path, data=data)

    def run_debug_plugin_release(self, data):
        path = 'plugin_releases/run_debug/'
        return self._post(path, data=data)

    def create_plugin_release(self, data):
        path = 'plugin_releases/'
        return self._post(path, data=data)

    def get_job(self, pk):
        path = f'jobs/{pk}/'
        return self._get(path)

    def list_jobs(self):
        path = 'jobs/'
        return self._get(path)

    def list_job_logs(self, pk):
        path = f'jobs/{pk}/logs/'
        return self._get(path)

    def tail_job_logs(self, pk):
        path = f'jobs/{pk}/tail_logs/'

        url = self._get_url(path)
        headers = self._get_headers()

        response = self.requests_session.get(url, headers=headers, stream=True)
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield f'{line}\n'

    def get_node(self, pk):
        path = f'nodes/{pk}/'
        return self._get(path)

    def list_nodes(self):
        path = 'nodes/'
        return self._get(path)

    def get_task(self, pk):
        path = f'tasks/{pk}/'
        return self._get(path)

    def list_tasks(self):
        path = 'tasks/'
        return self._get(path)
