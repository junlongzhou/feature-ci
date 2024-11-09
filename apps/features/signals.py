from django.dispatch import Signal
from django.dispatch import receiver
from json import dumps

from common.changes import FeatureChanges
from common.commands import FeatureCommand

feature_save = Signal()
post_feature_command = Signal()

@receiver(feature_save)
def post_save_feature_handler(sender, data, **kwargs):
    try:
        feature_json = dumps(data, indent=4)
        print(feature_json)
        feature_change = FeatureChanges(feature_json)
        feature_change.create()
    except Exception as e:
        print(e)

@receiver(post_feature_command)
def post_feature_command_handler(sender, feature_id, command_name, command_args, **kwargs):
    try:
        FeatureCommand(feature_id, command_name, command_args).post()
        return 'success'
    except Exception as e:
        return f'error: {e}'
