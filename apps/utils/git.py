from urllib.parse import urlsplit
from collections import namedtuple
from pathlib import Path
from subprocess import run
from os import environ
from tempfile import mktemp, mkdtemp
from requests import get
import re

GitUrl = namedtuple('GitUrl', ['protocol', 'hostname', 'port', 'path', 'username'])
GitRepo = namedtuple('GitRepo', ['repository', 'branch'])
GitMerge = namedtuple('GitMerge', ['repository', 'source_branch', 'target_branch'])
GitAuth = namedtuple('GitAuth', ['username', 'password', 'ssh_key'])

def parse_git_url(git_url):
    split_result = urlsplit(git_url)
    if git_url.startswith('git@'):
        split_result = urlsplit(f'ssh://{git_url}')
        port = split_result.netloc.split(':')[-1]
        path = split_result.path
        if not isinstance(port, int):
            path = f'{port}{path}'
            port = None
        return GitUrl(split_result.scheme, split_result.hostname, port, path, split_result.username)
    if not split_result.scheme:
        raise ValueError(f'Not supported git url: {git_url}')
    return GitUrl(split_result.scheme, split_result.hostname, split_result.port, split_result.path, split_result.username)

def parse_repo_path(git_url):
    return parse_git_url(git_url).path.lstrip('/').replace('.git', '')

def auth_config(git_url, username, password=None, ssh_key_file=None):
    if git_url.startswith('http') or git_url.startswith('https'):
        if not password:
            raise RuntimeError(f'Git password is missing for {git_url}')
        environ['GIT_TERMINAL_PROMPT'] = '0'
        run('rm -f ~/.git-credentials', shell=True, check=True)
        run('git config --global credential.helper store', shell=True, check=True)
        credential_file = mktemp()
        Path(credential_file).write_text(f'url={git_url}\nusername={username}\npassword={password}\n')
        run(f'cat {credential_file} | git credential approve', shell=True, check=True)
        Path(credential_file).unlink()
    else:
        if not Path(ssh_key_file).exists():
            raise RuntimeError(f'Git ssh_key_file is missing for {git_url}')
        run(f'sudo chmod 600 {ssh_key_file}', shell=True, check=True)
        run(f'git config --global core.sshCommand "ssh -i {ssh_key_file} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"',
            shell=True, check=True)

def clone(git_url, username=None, branch=None, bare=False, work_dir=None):
    if not git_url.startswith('git@')and username:
        url_parse_result = parse_git_url(git_url)
        if url_parse_result.username:
            git_url = git_url.replace(f'{url_parse_result.username}@', f'{username}@')
        else:
            git_url = git_url.replace(f'{url_parse_result.protocol}://', f'{url_parse_result.protocol}://{username}@')
    if not work_dir:
        work_dir = mkdtemp()
    options = []
    if bare:
        options.append('--bare')
    run(f'git clone {git_url} {" ".join(options)} .', cwd=work_dir, shell=True, check=True)
    if branch:
        cmd = f'git fetch origin {branch} && git checkout {branch}'
        if '/' in branch:
            local_branch = branch.replace('/', '-')
            cmd = f'git fetch origin {branch} && git checkout -b {local_branch} FETCH_HEAD && git checkout {local_branch}'
        run(cmd, cwd=work_dir, shell=True, check=True)
    return work_dir

def set_committer(username, email, global_config=True):
    options = ' --global' if global_config else ''
    run(f"git config{options} user.email '{email}'", shell=True, check=True)
    run(f"git config{options} user.name '{username}'", shell=True, check=True)

def add_hooks(hook_source, hook_name, repo_base_dir):
    repo_base_path = Path(repo_base_dir)
    git_hooks_path = repo_base_path / '.git' / 'hooks' / hook_name
    if Path(hook_source).exists():
        with git_hooks_path.open('w') as f:
            f.write(Path(hook_source).read_text())
    else:
        with get(hook_source, stream=True) as resp:
            with git_hooks_path.open('wb') as f:
                for chunk in resp.iter_content(chunk_size=512 * 1024):
                    f.write(chunk)
    git_hooks_path.chmod(0o755)

def commit(repo_base_dir, message, changes=['.'], rest_to_commit=None):
    if rest_to_commit:
        run(f'git reset {rest_to_commit}~1', cwd=repo_base_dir, shell=True, check=True)
    run(f"git add {' '.join(changes)}", cwd=repo_base_dir, shell=True, check=True)
    found_changes = run('git status --porcelain', cwd=repo_base_dir, shell=True, check=True, capture_output=True, text=True).stdout
    if not rest_to_commit and (not found_changes):
        print('Local repo are already update-to-date, nothing to commit.')
        return False
    commit_message_file = mktemp()
    Path(commit_message_file).write_text(message)
    run(f'git commit -F {commit_message_file}', cwd=repo_base_dir, shell=True, check=True)
    Path(commit_message_file).unlink()
    return True

def push(repo_base_dir, remote_name, dest_ref, push_options=[], force=False):
    options = [ f'-o {push_option}' for push_option in push_options]
    if force:
        options.append('--force')
    options = f" {' '.join(options)}" if options else ''
    run(f'git push {remote_name} {dest_ref}{options}', cwd=repo_base_dir, shell=True, check=True)

def log(repo_base_dir, format=None):
    options = ''
    if format:
        options = f' --format="{format}"'
    logs = run(f'git log{options}', cwd=repo_base_dir, shell=True, check=True, capture_output=True, text=True).stdout
    return logs if logs else ''

def merge(repo_base_dir, source_branch, target_branch, merge_options=[]):
    if source_branch == target_branch:
        print('Nothing to be merged.')
        return
    run(f'git fetch origin {target_branch}', cwd=repo_base_dir, shell=True, check=True)
    run(f'git checkout {target_branch}', cwd=repo_base_dir, shell=True, check=True)
    run(f'git merge {"".join(merge_options)} {source_branch}', cwd=repo_base_dir, shell=True, check=True)
    run(f'git push origin {target_branch}', cwd=repo_base_dir, shell=True, check=True)
    run(f'git push origin --delete {source_branch}', cwd=repo_base_dir, shell=True, check=True)

def get_head_commit(repo_base_dir):
    return run('git rev-parse HEAD', cwd=repo_base_dir, 
            shell=True, check=True, capture_output=True, text=True).stdout.strip()

def get_previous_tag(repo_base_dir, tag_regex, commit_id):
    tag_matcher = re.compile(tag_regex)
    previous_tag = run(f'git describe --abbrev=0 {commit_id}', cwd=repo_base_dir, 
        shell=True, check=True, capture_output=True, text=True).stdout.strip()
    while not tag_matcher.match(previous_tag):
        previous_tag = run(f'git describe --abbrev=0 {previous_tag}^', cwd=repo_base_dir, 
            shell=True, check=True, capture_output=True, text=True).stdout.strip()
    return previous_tag

def tag(repo_base_dir, name, message, force=False):
    run(f"git tag -a {name} -m'{message}'", cwd=repo_base_dir, shell=True, check=True)
    option = ' --force' if force else ''
    run(f"git push{option} origin {name}", cwd=repo_base_dir, shell=True, check=True)
