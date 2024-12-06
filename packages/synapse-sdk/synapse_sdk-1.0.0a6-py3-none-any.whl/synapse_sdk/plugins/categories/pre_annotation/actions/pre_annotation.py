from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import RunMethod, PluginCategory


@register_action
class PreAnnotationAction(Action):
    name = 'pre_annotation'
    category = PluginCategory.PRE_ANNOTATION
    method = RunMethod.TASK
