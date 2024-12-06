from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import RunMethod, PluginCategory


@register_action
class TrainAction(Action):
    name = 'train'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB

    def get_dataset(self):
        return {}

    def run(self):
        hyperparameter = self.params['hyperparameter']

        # download dataset
        self.log_event('Preparing dataset for training.')
        input_dataset = self.get_dataset()

        # train dataset
        self.log_event('Starting model training.')

        model_files = self.entrypoint(self, input_dataset, hyperparameter)

        # upload model_data
        self.log_event('Registering model data.')

        self.end_log()
        return model_files

    def log_metric(self, x, i, **kwargs):
        self.log(x, {x: i, **kwargs})

    def log_model(self, files, status=None):
        pass
