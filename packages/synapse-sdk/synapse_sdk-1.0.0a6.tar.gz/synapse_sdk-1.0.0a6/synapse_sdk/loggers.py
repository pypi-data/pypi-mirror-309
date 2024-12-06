import datetime

from synapse_sdk.clients.exceptions import ClientError


class BaseLogger:
    progress_records = {}

    def set_progress(self, current, total, category=''):
        percent = 0
        if total > 0:
            percent = (current / total) * 100
            percent = float(round(percent, 2))

        self.progress_records[category] = {'current': current, 'total': total, 'percent': percent}


class ConsoleLogger(BaseLogger):
    def set_progress(self, current, total, category=''):
        super().set_progress(current, total, category=category)
        print(self.progress_records)

    def log(self, action, data):
        print(action, data)


class BackendLogger(BaseLogger):
    logs_queue = []
    client = None
    job_id = None

    def __init__(self, client, job_id):
        self.client = client
        self.job_id = job_id

    def set_progress(self, current, total, category=''):
        super().set_progress(current, total, category=category)
        # TODO set_progress to the job

    def log(self, action, data):
        print(action, data)

        log = {
            'action': action,
            'data': data,
            'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'job': self.job_id,
        }
        self.logs_queue.append(log)
        try:
            self.client.create_logs(self.logs_queue)
            self.logs_queue.clear()
        except ClientError as e:
            print(e)
