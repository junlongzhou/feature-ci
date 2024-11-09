from argparse import ArgumentParser
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR / 'apps'))

from common.changes import FeatureChanges, DEFAULT_SERVER_CONFIG
from utils.gerrit import Change

def get_change(change_id):
    found_changes = Change.filter(DEFAULT_SERVER_CONFIG, f'change:{change_id}')
    if not found_changes:
        raise RuntimeError(f'Nothing changes found by ID {change_id}.')
    if len(found_changes) > 1:
        raise RuntimeError(f'More than one changes found by ID {change_id}: {found_changes}.')
    return found_changes[0]

def create_change_command(args):
    feature_json = args.feature_json
    if Path(args.feature_json).is_file():
        feature_json = Path(args.feature_json).read_text()
    FeatureChanges(feature_json).create()

def approve_change_command(args):
    found_change = get_change(args.change_id)
    found_change.status = args.status
    change_message = FeatureChanges.parse_change_message(found_change.current_message)
    FeatureChanges(change_message.body, existing_change=found_change).set_status()

def save_change_command(args):
    found_change = get_change(args.change_id)
    change_message = FeatureChanges.parse_change_message(found_change.current_message)
    FeatureChanges(change_message.body, existing_change=found_change).save()

def merge_change_command(args):
    found_change = get_change(args.change_id)
    change_message = FeatureChanges.parse_change_message(found_change.current_message)
    FeatureChanges(change_message.body, existing_change=found_change).merge(options=args.git_merge_option)

def tag_change_command(args):
    found_change = get_change(args.change_id)
    change_message = FeatureChanges.parse_change_message(found_change.current_message)
    FeatureChanges(change_message.body, existing_change=found_change).tag(args.tag_level_config_name, args.tag_prefix_config_name)

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--change_id', type=str, default='', help='The id of gerrit change.')

    subparsers = arg_parser.add_subparsers(required=True)
    # To create change via feature json
    create_change = subparsers.add_parser('create')
    create_change.add_argument('--feature_json', type=str, help='The json format of feature string or file name.')
    create_change.set_defaults(func=create_change_command)
    # To approve change via change id
    approve_change = subparsers.add_parser('approve')
    approve_change.add_argument('--status', type=str, choices=['wip'], default='wip', help='The status of approved gerrit change.')
    approve_change.set_defaults(func=approve_change_command)
    # To save change via change id
    save_change = subparsers.add_parser('save')
    save_change.set_defaults(func=save_change_command)
    # To merge change via change id
    merge_change = subparsers.add_parser('merge')
    merge_change.add_argument('--git_merge_option', type=str, nargs='*' ,default='', help='The id of gerrit change.')
    merge_change.set_defaults(func=merge_change_command)
    # To tag change via change id
    tag_change = subparsers.add_parser('tag')
    tag_change.add_argument('--tag_level_config_name', type=str, required=True, help='The config item name where to find the tag level from feature json.')
    tag_change.add_argument('--tag_prefix_config_name', type=str, default=None, help='The config item name where to find the tag prefix from feature json.')
    tag_change.set_defaults(func=tag_change_command)
    args = arg_parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
