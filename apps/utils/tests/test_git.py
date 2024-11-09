import pytest
from utils.git import parse_git_url, parse_repo_path, add_hooks, auth_config, \
    clone, set_committer, push, commit, merge, tag, get_head_commit, get_previous_tag
from pathlib import Path
from shutil import rmtree
from unittest import mock

@pytest.mark.parametrize('git_url,expected', [
    ('git@gitlabe1.ext.net.fci.com:rpm_specs/some_module_spec.git', 
        ('ssh', 'gitlabe1.ext.net.fci.com', None, 'rpm_specs/some_module_spec.git', 'git')
    ),
    ('ssh://fci_admin@gerrite1.ext.net.fci.com:8282/my-feature', 
        ('ssh', 'gerrite1.ext.net.fci.com', 8282, '/my-feature', 'fci_admin')
    ),
    ('git://fci_admin@gerrite1.ext.net.fci.com:8282/my-feature', 
        ('git', 'gerrite1.ext.net.fci.com', 8282, '/my-feature', 'fci_admin')
    ),
    ('git+ssh://gitlab.ext.net.fci.com/rpm_specs/my_module.git',
        ('git+ssh', 'gitlab.ext.net.fci.com', None, '/rpm_specs/my_module.git', None)
    ),
    ('ssh://fci_admin@gerrit.ext.net.fci.com:29418/my_group/my_subgroup/my_project.git',
      ('ssh', 'gerrit.ext.net.fci.com', 29418, '/my_group/my_subgroup/my_project.git', 'fci_admin')
    ),
    ('ssh://gerrit.ext.net.fci.com:29418/my_group/my_subgroup/my_project.git',
       ('ssh', 'gerrit.ext.net.fci.com', 29418, '/my_group/my_subgroup/my_project.git', None) 
    ),
    ('https://fci_admin@gerrit.ext.net.fci.com/my_group/my_subgroup/my_project.git',
       ('https', 'gerrit.ext.net.fci.com', None, '/my_group/my_subgroup/my_project.git', 'fci_admin') 
    ),
    ('ssh://git@gerrite1.ext.net.fci.com:8282/my_group/my_subgroup/my_project.git',
       ('ssh', 'gerrite1.ext.net.fci.com', 8282, '/my_group/my_subgroup/my_project.git', 'git')
    )
])
def test_parse_git_url(git_url, expected):
    parse_results = parse_git_url(git_url)
    assert (parse_results.protocol, parse_results.hostname, 
                parse_results.port, parse_results.path, parse_results.username) == expected

@pytest.mark.parametrize('git_url,expected', [
    ('git@gitlabe1.ext.net.fci.com:rpm_specs/some_module_spec.git', 'rpm_specs/some_module_spec'),
    ('https://fci_admin@gerrit.ext.net.fci.com/my_group/my_subgroup/my_project.git', 'my_group/my_subgroup/my_project'),
    ('ssh://git@gerrite1.ext.net.fci.com:8282/my_group/my_project', 'my_group/my_project'),
    ('ssh://git@gerrite1.ext.net.fci.com:8282/my_project', 'my_project')
])
def test_parse_repo_path(git_url, expected):
    assert parse_repo_path(git_url) == expected

@mock.patch('utils.git.Path')
@mock.patch('utils.git.mktemp')
@mock.patch('utils.git.run')
def test_auth_config_for_https_git_url(mock_run, mock_mktemp, mock_path):
    mock_mktemp.return_value = 'temp-file'
    mock_path.return_value = mock.MagicMock()
    auth_config('https://my.git.server.com', 'fci-admin', 'admin@fci')
    mock_run.assert_any_call('rm -f ~/.git-credentials', shell=True, check=True)
    mock_run.assert_any_call('git config --global credential.helper store', shell=True, check=True)
    mock_mktemp.assert_called()
    mock_path.assert_any_call('temp-file')
    mock_path.return_value.write_text.assert_called_with('url=https://my.git.server.com\nusername=fci-admin\npassword=admin@fci\n')
    mock_run.assert_any_call('cat temp-file | git credential approve', shell=True, check=True)
    mock_path.return_value.unlink.assert_called()

@mock.patch('utils.git.Path')
@mock.patch('utils.git.run')
def test_auth_config_for_ssh_git_url(mock_run, mock_path):
    mock_path.return_value = mock.MagicMock()
    mock_path.return_value.exists.return_value = True
    auth_config('ssh://my.git.server.com', 'fci-admin', ssh_key_file='fci-ssh-key')
    mock_path.assert_any_call('fci-ssh-key')
    mock_run.assert_any_call('sudo chmod 600 fci-ssh-key', shell=True, check=True)
    mock_run.assert_any_call('git config --global core.sshCommand "ssh -i fci-ssh-key -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"', shell=True, check=True)

@mock.patch('utils.git.mkdtemp')
@mock.patch('utils.git.run')
def test_clone_with_username(mock_run, mock_mktemp):
    mock_mktemp.return_value = 'temp-dir'
    repo_base_dir = clone('ssh://git@my.git.server.com/my-project.git', username='fci')
    mock_mktemp.assert_called()
    mock_run.assert_called_with('git clone ssh://fci@my.git.server.com/my-project.git  .', cwd='temp-dir', shell=True, check=True)
    assert repo_base_dir == 'temp-dir'

@mock.patch('utils.git.mkdtemp')
@mock.patch('utils.git.run')
def test_clone_with_gitlab_ssh_url(mock_run, mock_mktemp):
    mock_mktemp.return_value = 'temp-dir'
    repo_base_dir = clone('git@my.git.server.com/my-project.git', username='fci')
    mock_mktemp.assert_called()
    mock_run.assert_called_with('git clone git@my.git.server.com/my-project.git  .', cwd='temp-dir', shell=True, check=True)
    assert repo_base_dir == 'temp-dir'

@mock.patch('utils.git.mkdtemp')
@mock.patch('utils.git.run')
def test_clone_with_gerrit_change(mock_run, mock_mktemp):
    mock_mktemp.return_value = 'temp-dir'
    repo_base_dir = clone('git@my.git.server.com/my-project.git', branch='refs/changes/43/1699443/1', username='fci')
    mock_mktemp.assert_called()
    mock_run.assert_any_call('git clone git@my.git.server.com/my-project.git  .', cwd='temp-dir', shell=True, check=True)
    mock_run.assert_any_call('git fetch origin refs/changes/43/1699443/1 && git checkout -b refs-changes-43-1699443-1 FETCH_HEAD && git checkout refs-changes-43-1699443-1', cwd='temp-dir', shell=True, check=True)
    assert repo_base_dir == 'temp-dir'

@mock.patch('utils.git.mkdtemp')
@mock.patch('utils.git.run')
def test_clone_with_branch(mock_run, mock_mktemp):
    mock_mktemp.return_value = 'temp-dir'
    repo_base_dir = clone('ssh://git@my.git.server.com/my-project.git', branch='dev')
    mock_mktemp.assert_called()
    mock_run.assert_any_call('git clone ssh://git@my.git.server.com/my-project.git  .', cwd='temp-dir', shell=True, check=True)
    mock_run.assert_any_call('git fetch origin dev && git checkout dev', cwd='temp-dir', shell=True, check=True)
    assert repo_base_dir == 'temp-dir'

@mock.patch('utils.git.mkdtemp')
@mock.patch('utils.git.run')
def test_clone_with_bare(mock_run, mock_mktemp):
    mock_mktemp.return_value = 'temp-dir'
    repo_base_dir = clone('ssh://git@my.git.server.com/my-project.git', bare=True)
    mock_mktemp.assert_called()
    mock_run.assert_any_call('git clone ssh://git@my.git.server.com/my-project.git --bare .', cwd='temp-dir', shell=True, check=True)
    assert repo_base_dir == 'temp-dir'

def test_add_hooks_for_local(tmp_path):
    local_hook_file = Path(tmp_path) / 'local-hook'
    with local_hook_file.open('w') as f:
        f.write('dummy hook content')
    git_hooks_folder = Path(tmp_path) / 'my-project' / '.git' / 'hooks'
    git_hooks_folder.mkdir(parents=True)
    add_hooks(str(local_hook_file), 'commit-msg', git_hooks_folder.parent.parent)
    git_hook_file = Path(git_hooks_folder) / 'commit-msg'
    assert git_hook_file.is_file()
    assert git_hook_file.read_text() == 'dummy hook content'
    assert git_hook_file.stat().st_mode == 33206
    rmtree(tmp_path)

def test_add_hooks_for_remote(tmp_path):
    mocK_resp = mock.MagicMock()
    mocK_resp.__enter__.return_value.iter_content.return_value = [b'dummy hook content']
    with mock.patch('utils.git.get') as mock_get:
        mock_get.return_value = mocK_resp
        git_hooks_folder = Path(tmp_path) / 'my-project' / '.git' / 'hooks'
        git_hooks_folder.mkdir(parents=True)
        add_hooks('remote-hook', 'commit-msg', git_hooks_folder.parent.parent)
        git_hook_file = Path(git_hooks_folder) / 'commit-msg'
        assert git_hook_file.is_file()
        assert git_hook_file.read_text() == 'dummy hook content'
        assert git_hook_file.stat().st_mode == 33206
        rmtree(tmp_path)

@pytest.mark.parametrize('global_config,cmd_options',[
    (True, ' --global'),
    (False, ''),
])
def test_set_committer(global_config, cmd_options):
    with mock.patch('utils.git.run') as mock_run:
        set_committer('my-user', 'my-mail@mail.com', global_config=global_config)
        mock_run.assert_any_call(f"git config{cmd_options} user.email 'my-mail@mail.com'", shell=True, check=True)
        mock_run.assert_any_call(f"git config{cmd_options} user.name 'my-user'", shell=True, check=True)

@mock.patch('utils.git.mktemp')
@mock.patch('utils.git.Path')
@mock.patch('utils.git.run')
def test_commit_for_all_changes(mock_run, mock_path, mock_mktemp):
    mock_mktemp.return_value = 'temp-msg-file'
    mock_path.return_value = mock.MagicMock()
    mock_path.return_value.exists.return_value = True
    mock_run.return_value.stdout = 'New changes found.'
    commit('my-git-base-dir', 'Add for test\n\nThis is for test.')
    mock_run.assert_any_call('git add .', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git status --porcelain', cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_run.return_value.write_text('Add for test\n\nThis is for test.')
    mock_run.assert_any_call('git commit -F temp-msg-file', cwd='my-git-base-dir', shell=True, check=True)
    mock_path.assert_any_call('temp-msg-file')
    mock_path.return_value.unlink.assert_called()

@mock.patch('utils.git.mktemp')
@mock.patch('utils.git.Path')
@mock.patch('utils.git.run')
def test_commit_for_reset_to_commit(mock_run, mock_path, mock_mktemp):
    mock_mktemp.return_value = 'temp-msg-file'
    mock_path.return_value = mock.MagicMock()
    mock_path.return_value.exists.return_value = True
    mock_run.return_value.stdout = None
    commit('my-git-base-dir', 'Add for test\n\nThis is for test.', rest_to_commit='b69bc0e7daa5924e4c3023336023b40528430443')
    mock_run.assert_any_call('git add .', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git status --porcelain', cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_run.assert_any_call(f'git reset b69bc0e7daa5924e4c3023336023b40528430443~1', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.return_value.write_text('Add for test\n\nThis is for test.')
    mock_run.assert_any_call('git commit -F temp-msg-file', cwd='my-git-base-dir', shell=True, check=True)
    mock_path.assert_any_call('temp-msg-file')
    mock_path.return_value.unlink.assert_called()

@mock.patch('utils.git.mktemp')
@mock.patch('utils.git.Path')
@mock.patch('utils.git.run')
def test_commit_for_specific_changes(mock_run, mock_path, mock_mktemp):
    mock_mktemp.return_value = 'temp-msg-file'
    mock_path.return_value = mock.MagicMock()
    mock_path.return_value.exists.return_value = True
    mock_run.return_value.stdout = 'New changes found.'
    commit('my-git-base-dir', 'Add for test\n\nThis is for test.', changes=['change1', 'change2'])
    mock_run.assert_any_call('git add change1 change2', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git status --porcelain', cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_run.return_value.write_text('Add for test\n\nThis is for test.')
    mock_run.assert_any_call('git commit -F temp-msg-file', cwd='my-git-base-dir', shell=True, check=True)
    mock_path.assert_any_call('temp-msg-file')
    mock_path.return_value.unlink.assert_called()
    

@mock.patch('utils.git.mktemp')
@mock.patch('utils.git.Path')
@mock.patch('utils.git.run')
def test_commit_for_no_new_changes(mock_run, mock_path, mock_mktemp):
    mock_path.return_value = mock.MagicMock()
    mock_path.return_value.exists.return_value = True
    mock_run.return_value.stdout = None
    commit('my-git-base-dir', 'Add for test\n\nThis is for test.')
    mock_run.assert_any_call('git add .', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git status --porcelain', cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_mktemp.assert_not_called()
    mock_run.return_value.write_text.assert_not_called()
    mock_path.return_value.unlink.assert_not_called()

@mock.patch('utils.git.run')
def test_push_with_force(mock_run):
    push('my-git-base-dir', 'origin', 'HEAD:master', force=True)
    mock_run.assert_any_call('git push origin HEAD:master --force', cwd='my-git-base-dir', shell=True, check=True)

@mock.patch('utils.git.run')
def test_push_for_specific_changes_with_push_options(mock_run):
    push('my-git-base-dir', 'origin', 'HEAD:master', push_options=['wip', 'topic=my-topic'])
    mock_run.assert_any_call('git push origin HEAD:master -o wip -o topic=my-topic', cwd='my-git-base-dir', shell=True, check=True)

@mock.patch('utils.git.run')
def test_merge(mock_run):
    merge('my-git-base-dir', 'dev', 'master', merge_options=['-ff'])
    mock_run.assert_any_call('git fetch origin master', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git checkout master', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git merge -ff dev', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git push origin master', cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git push origin --delete dev', cwd='my-git-base-dir', shell=True, check=True)

@mock.patch('utils.git.run')
def test_merge_when_same_branches_given(mock_run):
    merge('my-git-base-dir', 'master', 'master')
    mock_run.assert_not_called()

@mock.patch('utils.git.run')
def test_get_head_commit(mock_run):
    mock_run.return_value.stdout = 'f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af'
    head_commit = get_head_commit('my-git-base-dir')
    mock_run.assert_any_call('git rev-parse HEAD', cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    assert head_commit == 'f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af'

@mock.patch('utils.git.run')
def test_get_previous_tag(mock_run):
    def return_tag(command, **kwargs):
        mock_return = mock.MagicMock()
        mock_return.stdout = {
            'git describe --abbrev=0 f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af': 'v3.5.0-1 ',
            'git describe --abbrev=0 v3.5.0-1^': 'v3.4.0-1 ',
            'git describe --abbrev=0 v3.4.0-1^': 'v3.3.0 '
        }[command]
        return mock_return
    mock_run.side_effect = return_tag
    pre_tag = get_previous_tag('my-git-base-dir', r'^[A-Za-z_-]*[0-9]+.[0-9]+.[0-9]+$', 'f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af')
    mock_run.assert_any_call('git describe --abbrev=0 f938ffdb26fc2a8f0a52429ae0a93d06bd8e22af',
        cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_run.assert_any_call('git describe --abbrev=0 v3.5.0-1^',
        cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    mock_run.assert_any_call('git describe --abbrev=0 v3.4.0-1^',
        cwd='my-git-base-dir', shell=True, check=True, capture_output=True, text=True)
    assert pre_tag == 'v3.3.0'

@mock.patch('utils.git.run')
def test_tag_with_force(mock_run):
    tag('my-git-base-dir', '3.5.0', 'My new tag\n\nMy message body', True)
    mock_run.assert_any_call("git tag -a 3.5.0 -m'My new tag\n\nMy message body'", 
        cwd='my-git-base-dir', shell=True, check=True)
    mock_run.assert_any_call('git push --force origin 3.5.0', 
        cwd='my-git-base-dir', shell=True, check=True)
