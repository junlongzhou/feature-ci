from unittest import mock
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from features.constants import Status, TemplateKind, FCI_ID_MAXIMUM_LEN, FCI_ID_PREFIX
from rest_framework import status
from features.utils import unique_fci_id
from features.models import Build

class TestApisTestCase(TestCase):

    def setUp(self) -> None:
        self.api_tester = User.objects.create(username='api-tester', password='api-tester', email='api-tester@test.com')
        self.user_token = Token.objects.create(user=self.api_tester).key
        self.api_client = Client()
        self.auth_headers = {'Authorization': f'Token {self.user_token}'}

    def test_component_api(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI1.0')
        component_metadata = {
            'repository': 'https://mygit/group/project.git',
            'main_branch': 'master',
            'properties': [
                {'name': 'category', 'value': 'container', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': '', 'values': ''
                }}
            ],
            'build': build.pk
        }
        # testing for creating new component
        resp = self.api_client.post('/api/v1/components/', data=component_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_component = resp.json()
        self.assertEqual(saved_component['repository'], component_metadata['repository'])
        self.assertEqual(saved_component['status'], Status.ACTIVE.name)
        self.assertEqual(saved_component['main_branch'], 'master')
        self.assertEqual(saved_component['build'], build.pk)
        self.assertEqual(saved_component['properties'][0]['name'], component_metadata['properties'][0]['name'])
        self.assertEqual(saved_component['properties'][0]['value'], component_metadata['properties'][0]['value'])
        self.assertEqual(saved_component['properties'][0]['style'], component_metadata['properties'][0]['style'])
        new_build = Build.objects.create(name='build1', status=Status.ACTIVE.value, product='FCI1.0')
        updated_component_metadata = {
            'repository': 'https://mygit/group/project-update.git',
            'properties': [
                {'name': 'category', 'value': 'pod', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
            ],
            'main_branch': 'mnt1',
            'build': new_build.pk
        }

        # testing for updating existing component
        put_resp = self.api_client.put(f'/api/v1/components/{saved_component["id"]}', data=updated_component_metadata, 
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK)
        updated_component = put_resp.json()
        self.assertEqual(updated_component['id'], saved_component['id'])
        self.assertEqual(updated_component['build'], new_build.pk)
        self.assertEqual(updated_component['main_branch'], 'mnt1')

        # testing for getting component detail
        find_component = self.api_client.get(f'/api/v1/components/{updated_component["id"]}').json()
        self.assertEqual(find_component['display_name'], 'group/project-update')
        self.assertDictEqual(find_component,  updated_component)

        # testing for getting components
        find_components = self.api_client.get(f'/api/v1/components/?repository=https://mygit/group/project-update.git').json()
        self.assertEqual(find_components['count'], 1)
        self.assertDictEqual(find_components['results'][0], updated_component)

         # testing for deleting component
        delete_resp = self.api_client.delete(f'/api/v1/components/{updated_component["id"]}',
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_build_api(self):
        build_metadata = {
            'name': 'release-product',
            'status': Status.PAUSE.value,
            'product': 'FCI-product',
            'property_templates': [
                {'kind': TemplateKind.FEATURE.name, 'name': 'main_branches', 'values': 'master,maintenance', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': '', 'values': ''
                }}
            ]
        }
        # test for creating new build
        resp = self.api_client.post('/api/v1/builds/', data=build_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_build = resp.json()
        self.assertEqual(saved_build['name'], build_metadata['name'])
        self.assertEqual(saved_build['product'], 'FCI-product')
        self.assertEqual(saved_build['status'], Status.PAUSE.name)
        self.assertEqual(saved_build['property_templates'][0]['name'], build_metadata['property_templates'][0]['name'])
        self.assertEqual(saved_build['property_templates'][0]['values'], build_metadata['property_templates'][0]['values'])
        self.assertEqual(saved_build['property_templates'][0]['kind'], build_metadata['property_templates'][0]['kind'])
        self.assertEqual(saved_build['property_templates'][0]['style'], build_metadata['property_templates'][0]['style'])

        # test for updating existing build
        updated_build_metadata = {
            'name': 'release-updated-product',
            'product': 'FCI-product1',
            'property_templates': [
                {'kind': TemplateKind.COMPONENT.name, 'name': 'main_branches', 'values': 'dev', 'style': {
                    'widget': 'select_multiple', 'read_only': False, 'hidden': False, 'command': '', 'values': ''
                }}
            ]
        }
        put_resp = self.api_client.put(f'/api/v1/builds/{saved_build["id"]}', data=updated_build_metadata,
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK, f'Actual: {put_resp.status_code}, {put_resp.json()}')
        updated_build = put_resp.json()
        self.assertEqual(updated_build['product'], 'FCI-product1')
        self.assertEqual(updated_build['id'], saved_build['id'])
        self.assertEqual(updated_build['property_templates'][0]['kind'], TemplateKind.COMPONENT.name)
        self.assertEqual(updated_build['property_templates'][0]['style'], updated_build_metadata['property_templates'][0]['style'])

        # test for getting build detail
        find_build = self.api_client.get(f'/api/v1/builds/{updated_build["id"]}').json()
        self.assertDictEqual(find_build, updated_build)

        # test for getting builds
        find_builds = self.api_client.get(f'/api/v1/builds/?name=release-updated-product').json()
        self.assertEqual(find_builds['count'], 1)
        self.assertDictEqual(find_builds['results'][0], updated_build)

        # test for deleting build
        delete_resp = self.api_client.delete(f'/api/v1/builds/{updated_build["id"]}',
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_feature_api(self):
        # init for build
        build_metadata = {
            'name': 'release-product',
            'status': Status.PAUSE.value,
            'product': 'FCI-product',
            'property_templates': [
                {'kind': TemplateKind.FEATURE.name, 'name': 'main_branches', 'values': 'master,maintenance', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
            ]
        }
        saved_build = self.api_client.post('/api/v1/builds/', data=build_metadata,
            headers=self.auth_headers, content_type='application/json').json()
        # init components
        component_one_resp = self.api_client.post('/api/v1/components/', 
            data={
                'repository': 'https://mygit/group/component-one.git',
                'properties': [
                    {'name': 'category', 'value': 'container', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        component_two_resp = self.api_client.post('/api/v1/components/',
            data={
                'repository': 'https://mygit/group/component-two.git',
                'properties': [
                    {'name': 'category', 'value': 'pod', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        component_three_resp = self.api_client.post('/api/v1/components/',
            data={
                'repository': 'https://mygit/group/component-three.git',
                'properties': [
                    {'name': 'category', 'value': 'subsystem', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        
        feature_metadata = {
            'name': 'first-feature', 'status': Status.ACTIVE.value, 'description': 'This is new feature',
            'last_update_author': self.api_tester.pk, 
            'properties': [{'name': 'priority', 'value': 'vip', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}],
            'changes': [
                {
                    'source_branch': 'dev-one', 
                    'component': component_one_resp.json()['id'],
                    'properties': [{'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                },
                {
                    'component': component_two_resp.json()['id'],
                    'properties': [{'name': 'merge', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                }
            ],
            'build': saved_build['id']
        }

        # test for creating new feature
        resp = self.api_client.post('/api/v1/features/', data=feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_feature = resp.json()
        self.assertEqual(saved_feature['name'], feature_metadata['name'])
        self.assertEqual(saved_feature['change_json'], f'/q/project:+subject:"{saved_feature["display_id"]}: {saved_feature["name"]}"')
        self.assertEqual(saved_feature['status'], Status.ACTIVE.name)
        self.assertEqual(saved_feature['description'], feature_metadata['description'])
        self.assertEqual(saved_feature['last_update_author'], self.api_tester.username)
        self.assertEqual(len(saved_feature['properties']), 1)
        self.assertEqual(saved_feature['properties'][0]['name'], feature_metadata['properties'][0]['name'])
        self.assertEqual(saved_feature['properties'][0]['value'], feature_metadata['properties'][0]['value'])
        feature_changes = saved_feature['changes']
        self.assertEqual(len(feature_changes), 2)
        self.assertSetEqual(set([ change['component'] for change in feature_changes]), 
            set([component_one_resp.json()['id'], component_two_resp.json()['id']]), f'{feature_changes}')
        changes_non_id_values = {}
        for change in feature_changes:
            change_properties = {}
            for property_item in change['properties']:
                change_properties[property_item['name']] = property_item['value']
            changes_non_id_values[change['component']] = (change['source_branch'], 
                change['target_branch'], change_properties)
        self.assertDictEqual(changes_non_id_values, {
            component_one_resp.json()['id']: ('dev-one', 'master', {'tag': 'true'}),
            component_two_resp.json()['id']: ('first-feature', 'master', {'merge': 'true'})
        })
        self.assertEqual(saved_feature['build'], saved_build['id'])

        # test for updating existing feature
        updated_feature_metadata = {
            'name': 'first-feature-update', 'status': Status.WIP.value, 'description': 'This is for updated feature',
            'last_update_author': self.api_tester.pk, 
            'properties': [{'name': 'priority', 'value': 'vip', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}],
            'changes': [
                {
                    'source_branch': 'master', 'target_branch': 'dev-one', 
                    'component': component_one_resp.json()['id'],
                    'properties': [{'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                },
                {
                    'source_branch': 'master', 'target_branch': 'dev-three', 
                    'component': component_three_resp.json()['id'],
                    'properties': [{'name': 'bump', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                }
            ],
            'build': saved_build['id']
        }
        str_fci_id = unique_fci_id(FCI_ID_PREFIX, saved_feature["id"], FCI_ID_MAXIMUM_LEN)
        put_resp = self.api_client.put(f'/api/v1/features/{str_fci_id}', data=updated_feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK, f'Actual: {put_resp.status_code}, {put_resp.json()}')
        updated_feature = put_resp.json()
        self.assertEqual(updated_feature['id'], saved_feature['id'])

        # test for getting feature detail
        find_feature = self.api_client.get(f'/api/v1/features/{str_fci_id}').json()
        self.assertDictEqual(find_feature, updated_feature)
        self.assertSetEqual(set([ change['component'] for change in find_feature['changes']]), 
            set([component_one_resp.json()['id'], component_three_resp.json()['id']]), f'Actual: {find_feature["changes"]}')
        self.assertEqual(find_feature['name'], updated_feature_metadata['name'])
        self.assertEqual(find_feature['status'], Status.WIP.name)
        self.assertEqual(find_feature['description'], updated_feature_metadata['description'])
        changes_non_id_values = {}
        for change in find_feature['changes']:
            change_properties = {}
            for property_item in change['properties']:
                change_properties[property_item['name']] = property_item['value']
            changes_non_id_values[change['component']] = (change['source_branch'], 
                change['target_branch'], change_properties, change['display_name'])
        self.assertDictEqual(changes_non_id_values, {
            component_one_resp.json()['id']: ('master', 'dev-one', {'tag': 'true'}, 'group/component-one'),
            component_three_resp.json()['id']: ('master', 'dev-three', {'bump': 'true'}, 'group/component-three')
        })

        # test for getting features
        find_features = self.api_client.get(f'/api/v1/features/?name=first-feature-update').json()
        self.assertEqual(find_features['count'], 1)
        self.assertDictEqual(find_features['results'][0], updated_feature)

        # test for partially updating existing feature
        partial_updated_feature_metadata = {
            'status': Status.ABANDONED.name, 'description': 'This is for partially updated feature',
        }
        patch_resp = self.api_client.patch(f'/api/v1/features/{saved_feature["id"]}', data=partial_updated_feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(patch_resp.json()['status'], 'ABANDONED')
        self.assertEqual(patch_resp.json()['description'], 'This is for partially updated feature')

        # test for deleting feature
        delete_resp = self.api_client.delete(f'/api/v1/features/{str_fci_id}',
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_feature_pretty_detail_api(self):
        # init for build
        build_metadata = {
            'name': 'release-product',
            'status': Status.PAUSE.value,
            'product': 'FCI-product',
            'property_templates': [
                {'kind': TemplateKind.FEATURE.name, 'name': 'main_branches', 'values': 'master,maintenance', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
            ]
        }
        saved_build = self.api_client.post('/api/v1/builds/', data=build_metadata,
            headers=self.auth_headers, content_type='application/json').json()
        # init components
        component_resp = self.api_client.post('/api/v1/components/', 
            data={
                'repository': 'https://mygit/group/component-one.git',
                'properties': [
                    {'name': 'category', 'value': 'container', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }},
                    {'name': 'need_bump', 'value': 'no', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        feature_metadata = {
            'name': 'test-for-feature-pretty', 'status': Status.ACTIVE.value,
            'description': 'This is test for feature pretty detail',
            'last_update_author': self.api_tester.pk, 
            'properties': [{'name': 'priority', 'value': 'vip', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}],
            'changes': [
                {
                    'component': component_resp.json()['id'],
                    'properties': [{'name': 'category', 'value': 'container1', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}, {'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                }
            ],
            'build': saved_build['id']
        }

        # init feature
        resp = self.api_client.post('/api/v1/features/', data=feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_feature = resp.json()
        str_fci_id = unique_fci_id(FCI_ID_PREFIX, saved_feature["id"], FCI_ID_MAXIMUM_LEN)
        find_feature = self.api_client.get(f'/api/v1/features/{str_fci_id}?pretty').json()
        self.assertEqual(find_feature['id'], 'FCI0000000000000000001')
        self.assertEqual(find_feature['name'], saved_feature['name'])
        self.assertEqual(find_feature['description'], saved_feature['description'])
        self.assertEqual(find_feature['last_update_author'], saved_feature['last_update_author'])
        self.assertEqual(find_feature['priority'], 'vip')
        self.assertListEqual(find_feature['changes'], [{
            'repository': 'https://mygit/group/component-one.git',
            'source_branch': 'test-for-feature-pretty', 'target_branch': 'master', 
            'category': 'container1',
            'need_bump': 'no',
            'tag': 'true'
        }], f'Actual: {find_feature["changes"]}')

    @mock.patch('utils.gerrit.Change.filter')
    def test_feature_command_api(self, mock_change_filter):
        mock_change_filter.return_value = [mock.MagicMock()]
        # init for build
        build_metadata = {
            'name': 'release-product',
            'status': Status.PAUSE.value,
            'product': 'FCI-product',
            'property_templates': [
                {'kind': TemplateKind.FEATURE.name, 'name': 'main_branches', 'values': 'master,maintenance', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
            ]
        }
        saved_build = self.api_client.post('/api/v1/builds/', data=build_metadata,
            headers=self.auth_headers, content_type='application/json').json()
        # init components
        component_resp = self.api_client.post('/api/v1/components/', 
            data={
                'repository': 'https://mygit/group/component-one.git',
                'properties': [
                    {'name': 'category', 'value': 'container', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        feature_metadata = {
            'name': 'test-for-feature-pretty', 'status': Status.ACTIVE.value,
            'description': 'This is test for feature pretty detail',
            'last_update_author': self.api_tester.pk, 
            'properties': [{'name': 'priority', 'value': 'vip', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}],
            'changes': [
                {
                    'source_branch': 'master', 'target_branch': 'dev-one', 
                    'component': component_resp.json()['id'],
                    'properties': [{'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                }
            ],
            'build': saved_build['id']
        }

        # init feature
        resp = self.api_client.post('/api/v1/features/', data=feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_feature = resp.json()
        resp = self.api_client.post(f'/api/v1/features/{saved_feature["id"]}/commands', data={
                'feature_id': saved_feature['id'],
                'command_name': 'run',
                'command_args': {'params': {'name1': 'value1'}}
            },
            headers=self.auth_headers, content_type='application/json')
        self.assertDictEqual(resp.json(),
            {'feature_id': int(saved_feature['id']), 'command_name': 'run', 'command_args': {'params': {'name1': 'value1'}}, 'message': 'success'},
            f'Actual: {resp.json()}')
        resp = self.api_client.post(f'/api/v1/features/{saved_feature["id"]}/commands', data={
                'feature_id': saved_feature['id'],
                'command_name': 'ok-to-test'
            },
            headers=self.auth_headers, content_type='application/json')
        self.assertDictEqual(resp.json(),
            {'feature_id': int(saved_feature['id']), 'command_name': 'ok-to-test', 'command_args': {}, 'message': 'success'},
            f'Actual: {resp.json()}')

    @mock.patch('utils.gerrit.Change.filter')
    def test_feature_action(self, mock_change_filter):
        mock_change_filter.return_value = [mock.MagicMock()]
        # init for build
        build_metadata = {
            'name': 'release-product',
            'status': Status.PAUSE.value,
            'product': 'FCI-product',
            'property_templates': [
                {'kind': TemplateKind.FEATURE.name, 'name': 'main_branches', 'values': 'master,maintenance', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
            ]
        }
        saved_build = self.api_client.post('/api/v1/builds/', data=build_metadata,
            headers=self.auth_headers, content_type='application/json').json()
        # init components
        component_resp = self.api_client.post('/api/v1/components/', 
            data={
                'repository': 'https://mygit/group/component-one.git',
                'properties': [
                    {'name': 'category', 'value': 'container', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}
                ],
                'main_branch': 'master',
                'build': saved_build['id']
            },
            headers=self.auth_headers, content_type='application/json')
        feature_metadata = {
            'name': 'test-for-approve-feature', 'status': Status.ACTIVE.name,
            'description': 'This is test for feature approve',
            'last_update_author': self.api_tester.pk, 
            'properties': [{'name': 'priority', 'value': 'vip', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}],
            'changes': [
                {
                    'source_branch': 'my-branch', 
                    'component': component_resp.json()['id'],
                    'properties': [{'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': ''
                }}]
                }
            ],
            'build': saved_build['id']
        }
        # init feature
        resp = self.api_client.post('/api/v1/features/', data=feature_metadata,
            headers=self.auth_headers, content_type='application/json')
        saved_feature = resp.json()
        self.assertTrue(resp.status_code==201, f'Actual status code: {resp.status_code}')
        self.assertDictEqual(saved_feature['changes'][0], {
            'component': 1,
            'display_name': 'group/component-one',
            'id': 1,
            'properties': [{'id': 2, 'name': 'tag', 'value': 'true', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False, 'command': '', 'values': ''
                }}],
            'repository': 'https://mygit/group/component-one.git',
            'source_branch': 'my-branch',
            'target_branch': 'master'
        }, f"Actual: {saved_feature['changes'][0]}"),
        patch_resp = self.api_client.patch(f'/api/v1/features/{saved_feature["id"]}', data={'action': 'approve'},
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(patch_resp.json()['status'], Status.WIP.name, f'Actual: {patch_resp.json()["status"]}')
        patch_resp = self.api_client.patch(f'/api/v1/features/{saved_feature["id"]}', data={'action': 'abandon'},
            headers=self.auth_headers, content_type='application/json')
        self.assertEqual(patch_resp.json()['status'], Status.ABANDONED.name, f'Actual: {patch_resp.json()["status"]}')
