from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import RunMethod, PluginCategory


@register_action
class InferenceAction(Action):
    name = 'inference'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.RESTAPI
