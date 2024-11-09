import pytest
from unittest import mock
from common.commands import FeatureCommand

@mock.patch('common.commands.ServerConfig')
@mock.patch('common.commands.Change.filter')
def test_feature_command_init_should_be_failed_when_no_change_found(mock_change_filter, mock_server_config):
    mock_change_filter.return_value = []
    mock_server_config.return_value = mock.MagicMock()
    with pytest.raises(RuntimeError, match='Nothing feature found by feature ID: FCI000001'):
        FeatureCommand('FCI000001', 'run', command_args={})
        mock_change_filter.assert_called_with(mock_server_config.return_value, 'project:+status:open+message:FCI000001')

@mock.patch('common.commands.ServerConfig')
@mock.patch('common.commands.Change.filter')
def test_feature_command_init_should_be_failed_when_more_than_one_change_found(mock_change_filter, mock_server_config):
    mock_change_filter.return_value = [{}, {}]
    mock_server_config.return_value = mock.MagicMock()
    with pytest.raises(RuntimeError, match='More than one feature found:'):
        FeatureCommand('FCI000001', 'run', command_args={})
        mock_change_filter.assert_called_with(mock_server_config.return_value, 'project:+status:open+message:FCI000001')

@mock.patch('common.commands.ServerConfig')
@mock.patch('common.commands.Change.filter')
def test_feature_command_post_should_set_correct_comment(mock_change_filter, mock_server_config):
    mock_change = mock.MagicMock()
    mock_change.set_comment.return_value = True
    mock_change_filter.return_value = [mock_change]
    mock_server_config.return_value = mock.MagicMock()
    FeatureCommand('FCI000001', 'run', command_args={'name': 'pipeline1', 'params': {'name1': 'value1', 'name2': 'value2'}}).post()
    mock_change_filter.assert_called_with(mock_server_config.return_value, 'project:+status:open+message:FCI000001')
    mock_change.set_comment.assert_called_with(mock_server_config.return_value, '/run pipeline1 --param name1=value1 --param name2=value2')

@mock.patch('common.commands.ServerConfig')
@mock.patch('common.commands.Change.filter')
def test_feature_command_post_should_set_correct_comment_when_empty_args_given(mock_change_filter, mock_server_config):
    mock_change = mock.MagicMock()
    mock_change.set_comment.return_value = True
    mock_change_filter.return_value = [mock_change]
    mock_server_config.return_value = mock.MagicMock()
    FeatureCommand('FCI000001', 'run', command_args={}).post()
    mock_change_filter.assert_called_with(mock_server_config.return_value, 'project:+status:open+message:FCI000001')
    mock_change.set_comment.assert_called_with(mock_server_config.return_value, '/run  ')
