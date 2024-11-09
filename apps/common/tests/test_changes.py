import pytest
from unittest import mock
from jsonschema import ValidationError
from common.changes import FeatureChanges
from utils.git import GitRepo, GitAuth, GitMerge
from utils.common import SemanticVersion, SEMANTIC_VERSION_REGEX

normally_feature_json = """
{
    "id": "FCI00000000001",
    "name": "first-feature",
    "status": "ACTIVE",
    "description": "This is new feature\\n\\nAdded: some backlog ID",
    "last_update_date": "2024-04-07T10:38:00.146734Z",
    "last_update_author": "admin",
    "abi_compatibility": "yes",
    "release_note": "feature",
    "main_branch": "my-branch",
    "changes": [
        {
            "repository": "git@gitlab.ext.net.fci.com:my-group/my-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "container",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "minor"
        },
        {
            "repository": "ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "pod",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "major"
        },
        {
            "repository": "https://github.ext.net.fci.com/some-group/some-project.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "spec",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "minor"
        },
        {
            "repository": "https://git@git.ext.net.fci.com/my-fci-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "code",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "patch"
        }
    ]
}
"""

normally_feature_json_contains_no_tag = """
{
    "id": "FCI00000000001",
    "name": "first-feature",
    "status": "ACTIVE",
    "description": "This is new feature\\n\\nAdded: some backlog ID",
    "last_update_date": "2024-04-07T10:38:00.146734Z",
    "last_update_author": "admin",
    "abi_compatibility": "yes",
    "release_note": "feature",
    "main_branch": "my-branch",
    "changes": [
        {
            "repository": "git@gitlab.ext.net.fci.com:my-group/my-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "container",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "no tag"
        },
        {
            "repository": "ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "pod",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "major"
        },
        {
            "repository": "https://github.ext.net.fci.com/some-group/some-project.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "spec",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "minor"
        },
        {
            "repository": "https://git@git.ext.net.fci.com/my-fci-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "code",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "patch"
        }
    ]
}
"""


feature_json_with_gerrit_changes = """
{
    "id": "FCI00000000001",
    "name": "first-feature",
    "status": "ACTIVE",
    "description": "This is new feature\\n\\nAdded: some backlog ID",
    "last_update_date": "2024-04-07T10:38:00.146734Z",
    "last_update_author": "admin",
    "abi_compatibility": "yes",
    "release_note": "feature",
    "main_branch": "my-branch",
    "changes": [
        {
            "repository": "git@gitlab.ext.net.fci.com:my-group/my-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "container",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "minor"
        },
        {
            "repository": "ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "pod",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "v",
            "tag_level": "major"
        },
        {
            "repository": "https://github.ext.net.fci.com/some-group/some-project.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "spec",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "minor"
        },
        {
            "repository": "https://git@git.ext.net.fci.com/my-fci-component.git",
            "target_branch": "master",
            "source_branch": "first-feature",
            "category": "code",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "patch"
        },
        {
            "repository": "https://git@gerrit.ext.net.fci.com/my-fci-component.git",
            "target_branch": "master",
            "source_branch": "refs/changes/05/5/2",
            "category": "code",
            "sw_changed": "true",
            "need_tag": "true",
            "need_merge": "true",
            "tag_prefix": "pq",
            "tag_level": "patch"
        }
    ]
}
"""

message_without_body = 'Some commit message'
message_without_change_id = '''Some commit message



Some commit message body


'''
message_normally = '''Some commit message

{
    "id": "FCI00000000001",
    "name": "first-feature",
    "status": "ACTIVE"
}


Change-Id: I7e4743a0fe0033445f0ca7fec18e869de91fa426


'''

def test_feature_init_json_is_invalid():
    with pytest.raises(ValueError) as errorInfo:
        FeatureChanges('{sasads')
        assert 'Invalid json format' in errorInfo.value

@pytest.mark.parametrize('init_json,expected_error', [
    ('{}', "'id' is a required property"), ('{"id": "FCI0001"}', "'name' is a required property"),
    ('{"id": "FCI0001", "name": "my-feature"}', "'description' is a required property"),
    ('{"id": "FCI0001", "name": "my-feature", "description": "my new feature", "status": "WIP"}', "'changes' is a required property")
])
def test_feature_init_json_not_contains_required_fields(init_json, expected_error):
    with pytest.raises(ValidationError, match=expected_error):
        FeatureChanges(init_json)

def test_feature_init_json_contains_required_fields():
    with mock.patch('common.changes.Change.filter') as mock_change_filter:
        mock_change_detail = mock.MagicMock()
        mock_change_detail.change_id = 'Id34abcfc077f78bd1b4867c6c35a1a1004c0016e'
        mock_change_detail.current_ref = 'refs/changes/81/1683881/3'
        mock_change_detail.current_revision = '68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d'
        mock_change_detail.current_message = 'Old message'
        mock_change_filter.return_value = [mock_change_detail]
        feature_change = FeatureChanges(normally_feature_json)
        args, _ = mock_change_filter.call_args
        assert len(args) == 2
        assert args[1] == 'project:+branch:my-branch+message:FCI00000000001'
        assert feature_change.change.topic == 'first-feature'
        assert feature_change.change.current_message == FeatureChanges.generate_change_message(feature_change.raw_data, 'Id34abcfc077f78bd1b4867c6c35a1a1004c0016e')
        assert feature_change.change.status == 'active'
        assert feature_change.change.branch == 'my-branch'
        assert feature_change.change.current_ref == 'refs/changes/81/1683881/3'
        assert feature_change.change.current_revision == '68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d'

def test_feature_init_json_when_change_does_not_exist():
    with mock.patch('common.changes.Change.filter') as mock_change_filter:
        mock_change_filter.return_value = []
        feature_change = FeatureChanges(normally_feature_json)
        args, _ = mock_change_filter.call_args
        assert len(args) == 2
        assert args[1] == 'project:+branch:my-branch+message:FCI00000000001'
        assert feature_change.change.topic == 'first-feature'
        assert feature_change.change.current_message == FeatureChanges.generate_change_message(feature_change.raw_data)
        assert feature_change.change.status == 'active'
        assert feature_change.change.branch == 'my-branch'
        assert feature_change.change.current_ref == 'my-branch'
        assert feature_change.change.current_revision is None

def test_feature_init_json_when_more_than_one_change_found():
    with pytest.raises(RuntimeError, match='More than one changes found chang-id-1,chang-id-2 from '):
        with mock.patch('common.changes.Change.filter') as mock_change_filter:
            mock_change1 = mock.MagicMock()
            mock_change1.change_id = 'chang-id-1'
            mock_change2 = mock.MagicMock()
            mock_change2.change_id = 'chang-id-2'
            mock_change_filter.return_value = [mock_change1, mock_change2]
            feature_change = FeatureChanges(normally_feature_json)
            args, _ = mock_change_filter.call_args
            assert len(args) == 2
            assert args[1] == 'project:+branch:my-branch+status:open+message:FCI00000000001'
            assert feature_change.change.topic == 'first-feature'
            assert feature_change.change.current_message == FeatureChanges.generate_change_message(feature_change.raw_data)
            assert feature_change.change.status == 'active'
            assert feature_change.change.branch == 'my-branch'
            assert feature_change.change.current_ref == 'my-branch'
            assert feature_change.change.current_revision is None

@mock.patch('common.changes.rmtree')
@mock.patch('common.changes.log')
@mock.patch('common.changes.Path')
@mock.patch('common.changes.clone')
@mock.patch('common.changes.auth_config')
def test_save_git_repo_logs(mock_auth_config, mock_clone, mock_path, mock_log, mock_rmtree):
    mock_clone.return_value = 'temp-repo-dir'
    mock_path.return_value = mock.MagicMock()
    FeatureChanges.save_git_repo_logs(GitRepo('http://my.git.server.com/my-group/my-project', 'main'),
        GitAuth('fci-admin', 'fci@admin', 'ssh.key'), 'temp-dir')
    mock_auth_config.assert_called_with('http://my.git.server.com/my-group/my-project', 'fci-admin', password='fci@admin', ssh_key_file='ssh.key')
    mock_path.assert_any_call('temp-dir')
    mock_log.assert_called_with('temp-repo-dir', format='%h %s')
    mock_rmtree.assert_called_with('temp-repo-dir')

@mock.patch('common.changes.rmtree')
@mock.patch('common.changes.FeatureChanges.save_git_repo_logs')
@mock.patch('common.changes.Change.filter')
@mock.patch('common.changes.commit')
@mock.patch('common.changes.push')
@mock.patch('common.changes.set_committer')
@mock.patch('common.changes.add_hooks')
@mock.patch('common.changes.clone')
@mock.patch('common.changes.auth_config')
def test_feature_change_save(mock_auth_config, mock_clone, mock_add_hooks, mock_set_committer,
        mock_push, mock_commit, mock_change_filter, mock_save_git_repo_logs, mock_rmtree):
    mock_clone.return_value = 'base-dir'
    mock_change_filter.return_value = []
    feature_change = FeatureChanges(normally_feature_json)
    feature_change.save()
    mock_save_git_repo_logs.assert_any_call(GitRepo('git@gitlab.ext.net.fci.com:my-group/my-component.git', 'master'), feature_change.git_auth, 'base-dir')
    mock_save_git_repo_logs.assert_any_call(GitRepo('ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git', 'master'), feature_change.git_auth, 'base-dir')
    mock_save_git_repo_logs.assert_any_call(GitRepo('https://github.ext.net.fci.com/some-group/some-project.git', 'master'), feature_change.git_auth, 'base-dir')
    mock_save_git_repo_logs.assert_any_call(GitRepo('https://git@git.ext.net.fci.com/my-fci-component.git', 'master'), feature_change.git_auth, 'base-dir')
    mock_auth_config.assert_any_call('/', '', password='', ssh_key_file=None)
    mock_clone.assert_called_with('/', '', 'my-branch')
    mock_add_hooks.assert_called_with('/tools/hooks/commit-msg', 'commit-msg', 'base-dir')
    mock_set_committer.assert_called_with('', '')
    mock_commit.assert_called_with('base-dir', feature_change.change.current_message, rest_to_commit=None)
    mock_push.assert_called_with('base-dir', 'origin', 'HEAD:refs/for/my-branch',
                push_options=[f'topic={feature_change.change.topic}'], force=True)
    mock_rmtree.assert_called_with('base-dir')

@mock.patch('common.changes.Change.create')
@mock.patch('common.changes.Change.filter')
def test_feature_create_when_change_does_not_exist(mock_change_filter, mock_change_create):
    mock_change_filter.return_value = []
    feature_change = FeatureChanges(normally_feature_json)
    feature_change.set_status = mock.MagicMock()
    feature_change.create()
    feature_change.set_status.assert_not_called()
    args, _ = mock_change_filter.call_args
    assert len(args) == 2
    assert args[1] == 'project:+branch:my-branch+message:FCI00000000001'
    mock_change_create.assert_called_with(feature_change.server_config, feature_change.change.project, 
        feature_change.change.branch, feature_change.change.current_message,
        feature_change.change.topic, is_private=True)

@mock.patch('common.changes.Change.set_commit_message')
@mock.patch('common.changes.Change.set_topic')
@mock.patch('common.changes.Change.filter')
def test_feature_create_when_change_found(mock_change_filter, mock_set_topic, mock_set_commit_message):
    mock_change_detail = mock.MagicMock()
    mock_change_detail.change_id = 'Id34abcfc077f78bd1b4867c6c35a1a1004c0016e'
    mock_change_detail.current_ref = 'refs/changes/81/1683881/3'
    mock_change_detail.current_revision = '68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d'
    mock_change_detail.current_message = 'Old message'
    mock_change_filter.return_value = [mock_change_detail]
    feature_change = FeatureChanges(normally_feature_json)
    feature_change.set_status = mock.MagicMock()
    feature_change.create()
    args, _ = mock_change_filter.call_args
    assert len(args) == 2
    assert args[1] == 'project:+branch:my-branch+message:FCI00000000001'
    mock_set_topic.assert_called_with(feature_change.server_config)
    mock_set_commit_message.assert_called_with(feature_change.server_config)
    feature_change.set_status.assert_called()

def test_parse_change_by_message_when_body_not_exist():
    with pytest.raises(RuntimeError, match='Invalid format: Message body is missing from'):
        FeatureChanges.parse_change_message(message_without_body)

def test_parse_change_by_message_when_change_id_not_exist():
    with pytest.raises(RuntimeError, match='Invalid format: Change-Id is missing from'):
        FeatureChanges.parse_change_message(message_without_change_id)

def test_parse_change_by_message():
    change_message = FeatureChanges.parse_change_message(message_normally)
    assert change_message.subject == 'Some commit message'
    assert change_message.body.strip() == '''{
    "id": "FCI00000000001",
    "name": "first-feature",
    "status": "ACTIVE"
}'''
    assert change_message.change_id == 'I7e4743a0fe0033445f0ca7fec18e869de91fa426'

@mock.patch('common.changes.merge')
@mock.patch('common.changes.rmtree')
@mock.patch('common.changes.clone')
@mock.patch('common.changes.auth_config')
def test_merge_git_branch(mock_auth_config, mock_clone, mock_rmtree, mock_merge):
    mock_clone.return_value = 'temp-dir'
    FeatureChanges.merge_git_branch(GitMerge('https://my.git.serve.com/myproject', 'dev', 'master'),
        GitAuth('my-name', 'my-passwd', 'my-key'), options=['-ff'])
    mock_auth_config.assert_called_with('https://my.git.serve.com/myproject', 'my-name', password='my-passwd', ssh_key_file='my-key')
    mock_clone.assert_called_with('https://my.git.serve.com/myproject', 'my-name', branch='dev')
    mock_merge.assert_called_with('temp-dir', 'dev', 'master', merge_options=['-ff'])
    mock_rmtree.assert_called_with('temp-dir')

@mock.patch('common.changes.rmtree')
@mock.patch('common.changes.tag')
@mock.patch('common.changes.get_previous_tag')
@mock.patch('common.changes.get_head_commit')
@mock.patch('common.changes.clone')
@mock.patch('common.changes.auth_config')
def test_tag_git_branch_head(mock_auth_config, mock_clone, mock_get_head_commit, mock_get_previous_tag, mock_tag, mock_rmtree):
    mock_clone.return_value = 'temp-dir'
    mock_get_head_commit.return_value = 'f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af'
    mock_get_previous_tag.return_value = 'v4.5.1'
    FeatureChanges.tag_git_branch_head(GitRepo('https://my.git.serve.com/myproject', 'master'),
        GitAuth('my-name', 'my-passwd', 'my-key'), SemanticVersion('minor', 'v'), 'My tag message body')
    mock_auth_config.assert_called_with('https://my.git.serve.com/myproject', 'my-name', password='my-passwd', ssh_key_file='my-key')
    mock_clone.assert_called_with('https://my.git.serve.com/myproject', 'my-name', branch='master')
    mock_get_head_commit.assert_called_with('temp-dir')
    mock_get_previous_tag.assert_called_with('temp-dir', SEMANTIC_VERSION_REGEX, 'f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af^')
    mock_tag.assert_called_with('temp-dir', 'v4.6.0', 'Automatic tag for v4.6.0\n\nMy tag message body')
    mock_rmtree.assert_called_with('temp-dir')

@mock.patch('common.changes.Change.filter')
@mock.patch('common.changes.FeatureChanges.merge_git_branch')
def test_feature_merge(mock_merge_git_branch, mock_filter):
    mock_filter.return_value = []
    feature_change = FeatureChanges(normally_feature_json)
    feature_change.merge()
    mock_merge_git_branch.assert_any_call(GitMerge('git@gitlab.ext.net.fci.com:my-group/my-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('https://github.ext.net.fci.com/some-group/some-project.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('https://git@git.ext.net.fci.com/my-fci-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])

@mock.patch('common.changes.FeatureChanges.find_component_change')
@mock.patch('common.changes.Change.filter')
@mock.patch('common.changes.FeatureChanges.merge_git_branch')
def test_feature_merge_with_gerrit_changes(mock_merge_git_branch, mock_filter, mock_find_component_change):
    mock_filter.return_value = []
    component_change = {
        "repository": "https://git@gerrit.ext.net.fci.com/my-fci-component.git",
        "target_branch": "master",
        "source_branch": "refs/changes/05/5/2",
        "category": "code",
        "sw_changed": "true",
        "need_tag": "true",
        "need_merge": "true",
        "tag_prefix": "pq",
        "tag_level": "patch"
    }
    mock_component_change = mock.MagicMock()
    mock_find_component_change.return_value = [mock_component_change]
    feature_change = FeatureChanges(feature_json_with_gerrit_changes)
    feature_change.merge()
    mock_merge_git_branch.assert_any_call(GitMerge('git@gitlab.ext.net.fci.com:my-group/my-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('https://github.ext.net.fci.com/some-group/some-project.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_merge_git_branch.assert_any_call(GitMerge('https://git@git.ext.net.fci.com/my-fci-component.git', 'first-feature', 'master'),
        feature_change.git_auth, options=[])
    mock_find_component_change.assert_called_with(feature_change.server_config, component_change)
    mock_component_change.submit.assert_called_with(feature_change.server_config)

@mock.patch('common.changes.Change.set_commit_message')
@mock.patch('common.changes.Change.filter')
@mock.patch('common.changes.FeatureChanges.tag_git_branch_head')
def test_feature_tag(mock_tag_git_branch_head, mock_filter, mock_set_commit_message):
    mock_filter.return_value = []
    mock_tag_git_branch_head.return_value = '3.4.5'
    feature_change = FeatureChanges(normally_feature_json_contains_no_tag)
    feature_change.tag('tag_level', 'tag_prefix')
    mock_tag_git_branch_head.assert_any_call(GitRepo('ssh://fci_admin@gerrit.ext.net.fci.com/my-another-component.git', 'master'),
        feature_change.git_auth, SemanticVersion('major', 'v'), 'FCI00000000001')
    mock_tag_git_branch_head.assert_any_call(GitRepo('https://github.ext.net.fci.com/some-group/some-project.git', 'master'),
        feature_change.git_auth, SemanticVersion('minor', 'pq'), 'FCI00000000001')
    mock_tag_git_branch_head.assert_any_call(GitRepo('https://git@git.ext.net.fci.com/my-fci-component.git', 'master'),
        feature_change.git_auth, SemanticVersion('patch', 'pq'), 'FCI00000000001')
    assert '"tag": "3.4.5"' in feature_change.change.current_message
    assert feature_change.change.current_message == FeatureChanges.generate_change_message(feature_change.raw_data, None)
    mock_set_commit_message.assert_called_with(feature_change.server_config)

@mock.patch('common.changes.Change.filter')
def test_find_component_changes(mock_change_filter):
    mock_change_filter.return_value = []
    server_config = mock.MagicMock()
    found_changes = FeatureChanges.find_component_change(server_config, {
        "repository": "https://git@gerrit.ext.net.fci.com/my-fci-component.git",
        "target_branch": "master",
        "source_branch": "refs/changes/05/5/2",
    })
    mock_change_filter.assert_called_with(server_config, 'project:my-fci-component+branch:master+change:5')
    assert found_changes == []

def test_generate_change_message_should_return_correct_message():
    message_without_change_id = FeatureChanges.generate_change_message({'id': 'FCI000001', 'name': 'my-feature', 'status': 'new'})
    assert message_without_change_id == 'FCI000001: my-feature\n\n{\n    "id": "FCI000001",\n    "name": "my-feature"\n}'
    message_with_change_id = FeatureChanges.generate_change_message({'id': 'FCI000001', 'name': 'my-feature', 'status': 'new'}, 'my-change-id')
    assert message_with_change_id == 'FCI000001: my-feature\n\n{\n    "id": "FCI000001",\n    "name": "my-feature"\n}\n\nChange-Id: my-change-id'
