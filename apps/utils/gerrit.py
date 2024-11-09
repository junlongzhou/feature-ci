from dataclasses import dataclass
from json import loads
from utils.http_request import make_retirable_session
import re

CHANGE_REF_REGEX = r'^refs/changes/[0-9]+/[0-9]+/[0-9]+$'

def is_gerrit_change(ref):
    return len(re.compile(CHANGE_REF_REGEX).findall(ref)) > 0

def parse_change_id(ref):
    return ref.split('/')[3]

@dataclass
class ChangeMessage:
    subject: str
    body: str
    change_id: str

@dataclass
class ServerConfig:
    server: str
    username: str
    password: str
    ssh_key: str = ''
    email: str = ''
    commit_msg_hook: str = 'tools/hooks/commit-msg'

@dataclass
class Change:
    project: str
    branch: str
    change_id: str
    subject: str
    status: str
    topic: str = ''
    current_revision: str = '' 
    current_ref: str = ''
    current_message: str = ''

    @classmethod
    def filter(cls, config: ServerConfig, query_str: str):
        session = make_retirable_session()
        if 'o=CURRENT_REVISION' not in query_str:
            query_str = f'{query_str}&o=CURRENT_REVISION'
        if 'o=CURRENT_COMMIT' not in query_str:
            query_str = f'{query_str}&o=CURRENT_COMMIT'
        url = f'{config.server}/a/changes/?q={query_str}'
        resp = session.get(url, auth=(config.username, config.password))
        found_changes = []
        if resp.ok:
            for change in loads(resp.text.split(")]}'")[-1]):
                current_revision, current_ref = change.get('current_revision', ''), ''
                if current_revision and change.get('revisions', {}).get(current_revision):
                    current_ref = change['revisions'][current_revision].get('ref', '')
                    current_message = change['revisions'][current_revision].get('commit', {}).get('message', '')
                found_changes.append(Change(
                    change.get('project', ''),
                    change.get('branch', ''),
                    change.get('change_id', ''),
                    change.get('subject', ''),
                    change.get('status', ''),
                    change.get('topic', ''),
                    current_revision,
                    current_ref,
                    current_message
                ))
        return found_changes
    
    @classmethod
    def create(cls, config: ServerConfig, project, branch, message, topic, is_private=False, work_in_progress=False):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/'
        resp = session.post(url, json={
                'project' : project,
                'subject' : message,
                'branch' : branch,
                'topic' : topic,
                'is_private': is_private,
                'work_in_progress': work_in_progress
            }, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok

    def set_commit_message(self, config: ServerConfig):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/{self.change_id}/message'
        resp = session.put(url, json={'message': self.current_message}, 
            auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
    
    def set_topic(self, config: ServerConfig):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/{self.change_id}/topic'
        resp = session.put(url, json={'topic': self.topic}, 
            auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
    
    def set_comment(self, config: ServerConfig, comment):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/{self.change_id}/revisions/{self.current_revision}/review'
        resp = session.post(url, json={'message': comment}, 
            auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
    
    def mark_private(self, config: ServerConfig, message=None):
        session = make_retirable_session()
        json_params = {'message': message} if message else None
        url = f'{config.server}/a/changes/{self.change_id}/private'
        resp = session.post(url, json=json_params, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
    
    def unmark_private(self, config: ServerConfig):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/{self.change_id}/private'
        resp = session.delete(url, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
    
    def set_work_in_progress(self, config: ServerConfig, message=None):
        session = make_retirable_session()
        json_params = {'message': message} if message else None
        url = f'{config.server}/a/changes/{self.change_id}/wip'
        resp = session.post(url, json=json_params, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok

    def abandon(self, config: ServerConfig, message=None):
        session = make_retirable_session()
        json_params = {'message': message} if message else None
        url = f'{config.server}/a/changes/{self.change_id}/abandon'
        resp = session.post(url, json=json_params, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok

    def submit(self, config: ServerConfig):
        session = make_retirable_session()
        url = f'{config.server}/a/changes/{self.change_id}/submit'
        resp = session.post(url, auth=(config.username, config.password))
        print(resp.text)
        resp.raise_for_status()
        return resp.ok
