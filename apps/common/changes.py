from json import loads, dumps
from os import environ
from pathlib import Path
from base64 import b64decode
from tempfile import mktemp
from shutil import rmtree
from jsonschema import validate
from copy import deepcopy
from utils.git import parse_repo_path, auth_config, clone, set_committer, commit, \
    push, log, add_hooks, merge, tag, get_head_commit, get_previous_tag, GitRepo, GitMerge, GitAuth
from utils.gerrit import Change, ServerConfig, ChangeMessage, is_gerrit_change, parse_change_id
from utils.common import bump_semantic_version, SemanticVersion, SEMANTIC_VERSION_REGEX, is_no_tag

GERRIT_URL = environ.get('GERRIT_URL', '')
GERRIT_REPO = environ.get('GERRIT_REPO', '')
GERRIT_USER = environ.get('GERRIT_USER', '')
GERRIT_EMAIL = environ.get('GERRIT_EMAIL', '')
GERRIT_PASSWORD = environ.get('GERRIT_PASSWORD', '')
GERRIT_COMMIT_MSG_HOOK = environ.get('GERRIT_COMMIT_MSG_HOOK', 'tools/hooks/commit-msg')
GERRIT_SSHKEY = environ.get('GERRIT_SSHKEY', '')
GERRIT_SSHKEY_FILE = None
if GERRIT_SSHKEY:
    GERRIT_SSHKEY_FILE = mktemp()
    Path(GERRIT_SSHKEY_FILE).write_bytes(b64decode(GERRIT_SSHKEY + '=='))

FEATURE_JSON_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'status': {'enum': ['PRIVATE', 'WIP', 'ACTIVE', 'MERGED', 'ABANDONED']},
        'changes': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'repository': {'type': 'string'},
                    'target_branch': {'type': 'string'},
                    'source_branch': {'type': 'string'}
                },
                'required': ['repository', 'target_branch', 'source_branch']
            },
            'minItems': 1,
        }
    },
    'required': ['id', 'name', 'description', 'changes'],
}

DEFAULT_SERVER_CONFIG = ServerConfig(GERRIT_URL, GERRIT_USER, GERRIT_PASSWORD, GERRIT_SSHKEY_FILE, GERRIT_EMAIL, GERRIT_COMMIT_MSG_HOOK)

class FeatureChanges(object):

    def __init__(self, feature_json:str, existing_change=None, gerrit_repo=GERRIT_REPO, server_config=DEFAULT_SERVER_CONFIG):
        try:
            self.raw_data = loads(feature_json)
        except Exception as e:
            raise ValueError(f'Invalid json format: {e}')
        validate(self.raw_data, FEATURE_JSON_SCHEMA)
        main_branch = self.raw_data.get('main_branch', 'master')
        self.gerrit_repo = gerrit_repo
        self.server_config = server_config
        self.git_auth = GitAuth(self.server_config.username, self.server_config.password, self.server_config.ssh_key)
        self.change = Change(project=self.gerrit_repo, branch=main_branch,
            change_id=None, subject=f"{self.raw_data['id']}: {self.raw_data['name']}",
            status=self.raw_data.get('status', '').lower(), topic=self.raw_data['name'],
            current_revision=None, current_ref=main_branch, 
            current_message=FeatureChanges.generate_change_message(self.raw_data))
        found_changes = []
        if existing_change:
            found_changes = [existing_change]
        else:
            found_changes = FeatureChanges.find_changes(self.server_config, self.gerrit_repo, self.change.branch, f"{self.raw_data['id']}")
        if len(found_changes) > 1:
            found_change_ids = ",".join([found_change.change_id for found_change in found_changes])
            raise RuntimeError(f'More than one changes found {found_change_ids} from {self.server_config.server}')
        if found_changes:
            print(f'Found change: {found_changes[0].change_id}')
            self.change.change_id = found_changes[0].change_id
            self.change.current_ref = found_changes[0].current_ref
            self.change.current_revision = found_changes[0].current_revision
            self.change.current_message = FeatureChanges.generate_change_message(self.raw_data, self.change.change_id)

    @classmethod
    def find_changes(cls, server_config, project, branch, message):
        query_str = f'project:{project}+branch:{branch}+message:{message}'
        return Change.filter(server_config, query_str)
    
    @classmethod
    def find_component_change(cls, server_config, change):
        change_id = parse_change_id(change['source_branch'])
        query_str = f"project:{parse_repo_path(change['repository'])}+branch:{change['target_branch']}+change:{change_id}"
        return Change.filter(server_config, query_str)

    @classmethod
    def save_git_repo_logs(cls, git_repo: GitRepo, git_auth: GitAuth, base_dir):
        change_folder = Path(base_dir) / f'{parse_repo_path(git_repo.repository)}'
        change_folder.mkdir(parents=True, exist_ok=True)
        auth_config(git_repo.repository, git_auth.username, password=git_auth.password, ssh_key_file=git_auth.ssh_key)
        change_repo_dir = clone(git_repo.repository, git_auth.username, branch=git_repo.branch)
        with (change_folder / 'git.log').open('w') as f:
            f.write(log(change_repo_dir, format='%h %s'))
        rmtree(change_repo_dir)

    @classmethod
    def generate_change_message(cls, feature_data, change_id=None):
        copied_feature_data = deepcopy(feature_data)
        if 'status' in copied_feature_data:
            del copied_feature_data['status']
        change_message = f"{copied_feature_data['id']}: {copied_feature_data['name']}\n\n{dumps(copied_feature_data, indent=4)}"
        if change_id:
            change_message = f'{change_message}\n\nChange-Id: {change_id}'
        return change_message

    @classmethod
    def parse_change_message(cls, message):
        message_splits = message.split('\n\n')
        if len(message_splits) < 2:
            raise RuntimeError(f'Invalid format: Message body is missing from {message}.')
        body = '\n\n'.join(message_splits[1:])
        if 'Change-Id:' not in body:
            raise RuntimeError(f'Invalid format: Change-Id is missing from {message}.')
        body_content, change_id = body.split('Change-Id:')
        return ChangeMessage(message_splits[0], body_content, change_id.strip())
    
    @classmethod
    def merge_git_branch(cls, git_merge: GitMerge, git_auth: GitAuth, options=[]):
        auth_config(git_merge.repository, git_auth.username, password=git_auth.password, ssh_key_file=git_auth.ssh_key)
        repo_dir = clone(git_merge.repository, git_auth.username, branch=git_merge.source_branch)
        merge(repo_dir, git_merge.source_branch, git_merge.target_branch, merge_options=options)
        rmtree(repo_dir)

    @classmethod
    def tag_git_branch_head(cls, git_repo: GitRepo, git_auth: GitAuth, semantic_version_config: SemanticVersion, message_body):
        auth_config(git_repo.repository, git_auth.username, password=git_auth.password, ssh_key_file=git_auth.ssh_key)
        repo_dir = clone(git_repo.repository, git_auth.username, branch=git_repo.branch)
        head_commit = get_head_commit(repo_dir)
        previous_tag = get_previous_tag(repo_dir, SEMANTIC_VERSION_REGEX, f'{head_commit}^')
        new_tag = bump_semantic_version(previous_tag, semantic_version_config)
        tag_message = f'Automatic tag for {new_tag}\n\n{message_body}'
        tag(repo_dir, new_tag, tag_message)
        rmtree(repo_dir)
        return new_tag

    def create(self):
        if not self.change.change_id:
            return Change.create(self.server_config, self.change.project, self.change.branch,
                self.change.current_message, self.change.topic, is_private=True)
        elif self.change.status.lower() != 'merged':
            self.set_status()
            return self.change.set_commit_message(self.server_config) and self.change.set_topic(self.server_config)

    def set_status(self):
        if 'wip' == self.change.status.lower():
            self.change.set_work_in_progress(self.server_config)
            self.change.unmark_private(self.server_config)
        elif 'abandoned' == self.change.status.lower():
            self.change.abandon(self.server_config)

    def save(self):
        feature_change_repo = f'{self.server_config.server}/{self.gerrit_repo}'
        auth_config(feature_change_repo, self.git_auth.username, password=self.git_auth.password, ssh_key_file=self.git_auth.ssh_key)
        base_dir = clone(feature_change_repo, self.git_auth.username, self.change.current_ref)
        for change in self.raw_data['changes']:
            FeatureChanges.save_git_repo_logs(GitRepo(change['repository'], change['target_branch']), self.git_auth, base_dir)
        add_hooks(f'{self.server_config.server}/{self.server_config.commit_msg_hook}', 'commit-msg', base_dir)
        set_committer(self.server_config.username, self.server_config.email)
        commit(base_dir, self.change.current_message, rest_to_commit=self.change.current_revision)
        auth_config(feature_change_repo, self.git_auth.username, password=self.git_auth.password, ssh_key_file=self.git_auth.ssh_key)
        push(base_dir, 'origin', f'HEAD:refs/for/{self.change.branch}',
                push_options=[f'topic={self.change.topic}'], force=True)
        rmtree(base_dir)

    def merge(self, options=[]):
        for change in self.raw_data['changes']:
            if is_gerrit_change(change['source_branch']):
                found_component_changes = FeatureChanges.find_component_change(self.server_config, change)
                if not found_component_changes:
                    raise RuntimeError(f'Nothing changes found by {change}')
                found_component_changes[0].submit(self.server_config)
            else:
                FeatureChanges.merge_git_branch(GitMerge(change['repository'], change['source_branch'], change['target_branch']),
                    self.git_auth, options=options)

    def tag(self, tag_level_config_name, tag_prefix_config_name=None):
        for change in self.raw_data['changes']:
            tag_prefix = change.get(tag_prefix_config_name, '') if tag_prefix_config_name else ''
            tag_level = change.get(tag_level_config_name) if tag_level_config_name else ''
            if is_no_tag(tag_level):
                continue
            change['tag'] = FeatureChanges.tag_git_branch_head(GitRepo(change['repository'], change['target_branch']), self.git_auth,
                SemanticVersion(tag_level, tag_prefix), self.raw_data['id'])
        self.change.current_message = FeatureChanges.generate_change_message(self.raw_data, self.change.change_id)
        self.change.set_commit_message(self.server_config)
