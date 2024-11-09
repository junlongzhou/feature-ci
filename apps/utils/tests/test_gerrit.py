import pytest
from unittest import mock
from utils.gerrit import Change, ServerConfig

query_changes_response = '''
)]}'
[
    {
        "project": "my-project",
        "branch": "master",
        "change_id": "Id34abcfc077f78bd1b4867c6c35a1a1004c0016e",
        "subject": "FCI: first-feature(FCI00000000001)",
        "status": "new",
        "topic": "first-feature",
        "current_revision": "68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d",
        "revisions": {
            "68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d": {
                "ref": "refs/changes/81/1683881/3"
            }
        }
    }
]
'''

def test_change_filter_when_changes_found():
    config = ServerConfig('https://my.gerrit.ext.com', 'fci-admin', 'admin@fci')
    with mock.patch('utils.gerrit.make_retirable_session') as mock_make_retirable_session:
        mock_session_return = mock.MagicMock()
        mock_make_retirable_session.return_value = mock_session_return
        mock_session_return.get.return_value.ok = True
        mock_session_return.get.return_value.text = query_changes_response
        found_changes = Change.filter(config, 'project:my-project+branch:master+status:open&o=CURRENT_REVISION')
        assert len(found_changes) == 1
        assert found_changes[0].project == 'my-project'
        assert found_changes[0].branch == 'master'
        assert found_changes[0].change_id == 'Id34abcfc077f78bd1b4867c6c35a1a1004c0016e'
        assert found_changes[0].subject == 'FCI: first-feature(FCI00000000001)'
        assert found_changes[0].status == 'new'
        assert found_changes[0].topic == 'first-feature'
        assert found_changes[0].current_revision == '68f79a45889c270dc86a9e0ec1f6e6d2d2c8781d'
        assert found_changes[0].current_ref == 'refs/changes/81/1683881/3'
        mock_session_return.get.assert_called_with(
            'https://my.gerrit.ext.com/a/changes/?q=project:my-project+branch:master+status:open&o=CURRENT_REVISION&o=CURRENT_COMMIT',
            auth=('fci-admin', 'admin@fci'))
        
def test_change_filter_when_no_changes_found():
    config = ServerConfig('https://my.gerrit.ext.com', 'fci-admin', 'admin@fci')
    with mock.patch('utils.gerrit.make_retirable_session') as mock_make_retirable_session:
        mock_session_return = mock.MagicMock()
        mock_make_retirable_session.return_value = mock_session_return
        mock_session_return.get.return_value.ok = False
        found_changes = Change.filter(config, 'project:my-project+branch:master+status:open&o=CURRENT_REVISION')
        assert len(found_changes) == 0
        mock_session_return.get.assert_called_with(
            'https://my.gerrit.ext.com/a/changes/?q=project:my-project+branch:master+status:open&o=CURRENT_REVISION&o=CURRENT_COMMIT',
            auth=('fci-admin', 'admin@fci'))

def test_change_set_commit_message():
    config = ServerConfig('https://my.gerrit.ext.com', 'fci-admin', 'admin@fci')
    with mock.patch('utils.gerrit.make_retirable_session') as mock_make_retirable_session:
        mock_session_return = mock.MagicMock()
        mock_make_retirable_session.return_value = mock_session_return
        mock_session_return.put.return_value.ok = True
        mock_session_return.put.return_value.raise_for_status.return_value = None
        res = Change('', '', 'my-change-id', '', '', current_message='my-message').set_commit_message(config)
        mock_session_return.put.assert_called_with('https://my.gerrit.ext.com/a/changes/my-change-id/message',
            json={'message': 'my-message'}, auth=('fci-admin', 'admin@fci'))
        mock_session_return.put.return_value.raise_for_status.assert_called()
        assert res == True

def test_change_set_topic():
    config = ServerConfig('https://my.gerrit.ext.com', 'fci-admin', 'admin@fci')
    with mock.patch('utils.gerrit.make_retirable_session') as mock_make_retirable_session:
        mock_session_return = mock.MagicMock()
        mock_make_retirable_session.return_value = mock_session_return
        mock_session_return.put.return_value.ok = True
        mock_session_return.put.return_value.raise_for_status.return_value = None
        res = Change('', '', 'my-change-id', '', '', topic='my-topic').set_topic(config)
        mock_session_return.put.assert_called_with('https://my.gerrit.ext.com/a/changes/my-change-id/topic',
            json={'topic': 'my-topic'}, auth=('fci-admin', 'admin@fci'))
        mock_session_return.put.return_value.raise_for_status.assert_called()
        assert res == True

def test_change_set_comment():
    config = ServerConfig('https://my.gerrit.ext.com', 'fci-admin', 'admin@fci')
    with mock.patch('utils.gerrit.make_retirable_session') as mock_make_retirable_session:
        mock_session_return = mock.MagicMock()
        mock_make_retirable_session.return_value = mock_session_return
        mock_session_return.post.return_value.ok = True
        mock_session_return.post.return_value.raise_for_status.return_value = None
        res = Change('', '', 'my-change-id', '', '', current_revision='my-revision').set_comment(config, 'my-comment')
        mock_session_return.post.assert_called_with('https://my.gerrit.ext.com/a/changes/my-change-id/revisions/my-revision/review',
            json={'message': 'my-comment'}, auth=('fci-admin', 'admin@fci'))
        mock_session_return.post.return_value.raise_for_status.assert_called()
        assert res == True
