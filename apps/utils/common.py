from dataclasses import dataclass

SEMANTIC_VERSION_REGEX = r'^[A-Za-z_-]*[0-9]+.[0-9]+.[0-9]+$'

@dataclass
class SemanticVersion:
    change_level: str
    prefix: str = ''

def is_no_tag(change_level):
    return not change_level or change_level.lower() == 'no tag'

def bump_semantic_version(previous_version, semantic_version: SemanticVersion):
    change_level = semantic_version.change_level.lower()
    previous_version_without_prefix = previous_version.split(semantic_version.prefix)[-1] if semantic_version.prefix else previous_version
    previous_version_splits = previous_version_without_prefix.split('.')
    if len(previous_version_splits) != 3 :
        raise RuntimeError(f'Wrong version format in previous tag - expected MAJOR.MINOR.PATCH - got {previous_version}')
    if change_level not in ['major', 'minor', 'patch']:
        raise RuntimeError(f'Change level {change_level} is not supported - expected major|minor|patch')
    if any([ not part_version.isdigit() for part_version in previous_version_splits ]):
        raise RuntimeError(f'Wrong version format in previous tag - expected [0-9]+.[0-9]+.[0-9]+ - got {previous_version}')
    major, minor, patch = previous_version_splits
    new_version = ''
    if change_level == 'major':
        new_version = f'{semantic_version.prefix}{int(major) + 1}.0.0'
    elif change_level == 'minor':
        new_version = f'{semantic_version.prefix}{major}.{int(minor) + 1}.0'
    else:
        new_version = f'{semantic_version.prefix}{major}.{minor}.{int(patch) + 1}'
    return new_version
