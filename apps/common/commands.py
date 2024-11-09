from os import environ
from utils.gerrit import Change, ServerConfig

GERRIT_URL = environ.get('GERRIT_URL', '')
GERRIT_REPO = environ.get('GERRIT_REPO', '')
GERRIT_USER = environ.get('GERRIT_USER', '')
GERRIT_USER_MAIL = environ.get('GERRIT_USER_MAIL', '')
GERRIT_PASSWORD = environ.get('GERRIT_PASSWORD', '')

class FeatureCommand:

    def __init__(self, feature_id, command_name, command_args=None) -> None:
        self.server_config = ServerConfig(GERRIT_URL, GERRIT_USER, GERRIT_PASSWORD)
        found_changes = Change.filter(self.server_config, f'project:{GERRIT_REPO}+status:open+message:{feature_id}')
        if not found_changes:
            raise RuntimeError(f'Nothing feature found by feature ID: {feature_id}')
        if len(found_changes) > 1:
            raise RuntimeError(f'More than one feature found: {found_changes}')
        self.change = found_changes[0]
        self.command_name = command_name
        self.command_args = command_args

    def post(self):
        name, params = '', []
        if self.command_args:
            name = self.command_args.get('name', '')
            for param_name, param_value in self.command_args.get('params', {}).items():
                params.append(f'--param {param_name}={param_value}')
        self.change.set_comment(self.server_config, f'/{self.command_name} {name} {" ".join(params)}')
