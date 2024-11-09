import pytest
from utils.common import bump_semantic_version, SemanticVersion

def test_bump_semantic_version_should_failed_when_wrong_format_given():
    with pytest.raises(RuntimeError, match='Wrong version format in previous tag - expected MAJOR.MINOR.PATCH - got'):
        bump_semantic_version('v2.5-4', SemanticVersion('major', 'v'))

def test_bump_semantic_version_should_failed_when_non_digit_versions_given():
    with pytest.raises(RuntimeError, match='Wrong version format in previous tag - expected'):
        bump_semantic_version('v2.5.nok4', SemanticVersion('major', 'v'))

def test_bump_semantic_version_should_failed_when_wrong_change_level_given():
    with pytest.raises(RuntimeError, match='Change level other is not supported - expected major|minor|patch'):
        bump_semantic_version('v2.5.4', SemanticVersion('other', 'v'))

def test_bump_semantic_version_should_success_when_prefix_not_given():
    new_version = bump_semantic_version('2.5.4', SemanticVersion('major'))
    new_version == '3.0.0'

def test_bump_semantic_version_should_success_when_minor_given():
    new_version = bump_semantic_version('2.5.4', SemanticVersion('minor'))
    new_version == '2.6.0'

def test_bump_semantic_version_should_success_when_patch_given():
    new_version = bump_semantic_version('2.5.4', SemanticVersion('patch'))
    new_version == '2.5.5'
