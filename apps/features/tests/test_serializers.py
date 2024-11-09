from django.test import TestCase
from features.serializers import BuildSerializer, ComponentSerializer, FeatureSerializer
from features.models import Build, PropertyTemplate, Component, Property, Feature, User, ComponentChange
from features.constants import Status, TemplateKind

class FeatureSerializersTestCase(TestCase):

    def test_create_build(self):
        build_serializer = BuildSerializer(data={'name': 'new build',
            'status': Status.PAUSE.value, 'property_templates': [
                {'name': 'name1', 'values': 'value1', 'status': Status.ACTIVE.value, 'kind': TemplateKind.FEATURE.name, 'style': {
                    'widget': 'text', 'read_only': False, 'hidden': False
                }},
                {'name': 'name2', 'values': 'value2', 'status': Status.ACTIVE.value, 'kind': TemplateKind.COMPONENT.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}
            ], 'product': 'FCI2.0'})
        self.assertTrue(build_serializer.is_valid(), f'Actual error: {build_serializer.errors}')
        new_build = build_serializer.save()
        build_in_db = Build.objects.get(pk=new_build.pk)
        self.assertEqual(build_in_db, new_build)
        self.assertEqual(build_in_db.name, 'new build')
        self.assertEqual(build_in_db.status, Status.PAUSE.value)
        self.assertEqual(build_in_db.product, 'FCI2.0')
        property_templates_queryset = PropertyTemplate.objects.filter(build=build_in_db)
        self.assertEqual(property_templates_queryset.count(), 2)
        self.assertSetEqual(
            set([ property_template.name for property_template in property_templates_queryset]),
            set(['name1', 'name2']))
        self.assertSetEqual(
            set([ property_template.values for property_template in property_templates_queryset]),
            set(['value1', 'value2']))
        self.assertSetEqual(
            set([ property_template.kind for property_template in property_templates_queryset]),
            set([TemplateKind.FEATURE.name, TemplateKind.COMPONENT.name]))
        self.assertSetEqual(
            set([property_template.style for property_template in property_templates_queryset]),
            set(['widget:text;read_only:false;hidden:false;command:;values:;', 'widget:select;read_only:false;hidden:false;command:;values:;']))
        
    def test_update_build(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI1.0')
        PropertyTemplate.objects.create(build=build, name='name1', values='value,value2',
            kind=TemplateKind.FEATURE.name, status=Status.ACTIVE.value)
        build_serializer = BuildSerializer(build, data={'name': 'update build',
            'status': Status.ACTIVE.value, 'property_templates': [
                {'name': 'name1', 'values': 'value1', 'status': Status.ACTIVE.value,'kind': TemplateKind.FEATURE.name, 'style': {
                    'widget': 'text', 'read_only': False, 'hidden': False
                }},
                {'name': 'name2', 'values': 'value2', 'status': Status.ACTIVE.value, 'kind': TemplateKind.COMPONENT.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}
            ], 'product': 'FCI2.0'})
        self.assertTrue(build_serializer.is_valid(), f'Actual error: {build_serializer.errors}')
        updated_build = build_serializer.save()
        build_in_db = Build.objects.get(pk=build.pk)
        self.assertEqual(build_in_db, updated_build)
        self.assertEqual(build_in_db.name, 'update build')
        self.assertEqual(build_in_db.status, Status.ACTIVE.value)
        property_templates_queryset = PropertyTemplate.objects.filter(build=build_in_db)
        self.assertEqual(property_templates_queryset.count(), 2)
        self.assertSetEqual(
            set([ property_template.name for property_template in property_templates_queryset]),
            set(['name1', 'name2']))
        self.assertSetEqual(
            set([ property_template.values for property_template in property_templates_queryset]),
            set(['value1', 'value2']))
        self.assertSetEqual(
            set([ property_template.kind for property_template in property_templates_queryset]),
            set([TemplateKind.FEATURE.name, TemplateKind.COMPONENT.name]))
        self.assertSetEqual(
            set([property_template.style for property_template in property_templates_queryset]),
            set(['widget:text;read_only:false;hidden:false;command:;values:;', 'widget:select;read_only:false;hidden:false;command:;values:;']))
    
    def test_create_component(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI2.0')
        component_serializer = ComponentSerializer(data={
            'repository': 'https://git1.ext.com/group/project',
            'status': Status.ACTIVE.value,
            'main_branch': 'master',
            'build': build.pk,
            'properties': [
                {'name': 'name1', 'value': 'value1', 'style': {
                    'widget': 'text', 'read_only': False, 'hidden': False
                }},
                {'name': 'name2', 'value': 'value2', 'style': {
                    'widget': 'text', 'read_only': False, 'hidden': False
                }}
            ]
        })
        self.assertTrue(component_serializer.is_valid(), f'Actual error: {component_serializer.errors}')
        new_component = component_serializer.save()
        self.assertEqual(new_component, Component.objects.get(pk=new_component.pk))
        self.assertEqual(new_component.repository, 'https://git1.ext.com/group/project')
        self.assertEqual(new_component.status, Status.ACTIVE.value)
        self.assertEqual(new_component.main_branch, 'master')
        self.assertEqual(new_component.build.pk, build.pk)
        properties = Property.objects.filter(component=new_component)
        self.assertEqual(properties.count(), 2)
        self.assertSetEqual(set([ item.name for item in properties]), set(['name1', 'name2']))
        self.assertSetEqual(set([ item.value for item in properties]), set(['value1', 'value2']))

    def test_update_component(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI2.0')
        component = Component.objects.create(repository='https://git1.ext.com/group/project',
            build=build, main_branch='main', status=Status.ACTIVE.value)
        Property.objects.create(name='category1', value='container', component=component)
        new_build = Build.objects.create(name='new_build', status=Status.ACTIVE.value, product='FCI2.0')
        component_serializer = ComponentSerializer(component, data={
            'repository': 'https://git1.ext.com/group/project1',
            'status': Status.ACTIVE.value,
            'main_branch': 'master',
            'build': new_build.pk,
            'properties': [
                {'name': 'category1', 'value': 'value1', 'style': {
                    'widget': 'text', 'read_only': False, 'hidden': False
                }},
                {'name': 'category2', 'value': 'value2', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}
            ]
        })
        self.assertTrue(component_serializer.is_valid(), f'Actual error: {component_serializer.errors}')
        saved_component = component_serializer.save()
        updated_component = Component.objects.get(pk=component.pk)
        self.assertEqual(Component.objects.filter(repository='https://git1.ext.com/group/project1').count(), 1)
        self.assertEqual(component, updated_component)
        self.assertEqual(updated_component.repository, 'https://git1.ext.com/group/project1')
        self.assertEqual(updated_component.status, Status.ACTIVE.value)
        self.assertEqual(component, updated_component)
        self.assertEqual(saved_component.main_branch, updated_component.main_branch)
        self.assertEqual(new_build, updated_component.build)
        properties = Property.objects.filter(component=updated_component)
        self.assertEqual(properties.count(), 2)
        self.assertSetEqual(set([item.name for item in properties]), set(['category1', 'category2']))
        self.assertSetEqual(set([item.value for item in properties]), set(['value1', 'value2']))

    def test_create_feature_when_changes_not_given(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI2.0')
        user = User.objects.create(username='user1')
        feature_serializer = FeatureSerializer(data={
            'name': 'feature1', 'status': Status.ACTIVE.value, 'description': 'new feature',
            'last_update_author': user.pk, 
            'properties': [{'name': 'category1', 'value': 'value1', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}],
            'build': build.pk
        })
        self.assertFalse(feature_serializer.is_valid())
        self.assertTrue(len(feature_serializer.errors))

    def test_create_feature_when_properties_not_given(self):
        build = Build.objects.create(name='build', status=Status.ACTIVE.value, product='FCI2.0')
        user = User.objects.create(username='user1')
        component = Component.objects.create(repository='https://git1.ext.com/group/project', main_branch='master', build=build, status=Status.ACTIVE.value)
        feature_serializer = FeatureSerializer(data={
            'name': 'feature1', 'status': Status.ACTIVE.value, 'description': 'new feature',
            'last_update_author': user.pk, 
            'changes': [{'source_branch': 'master', 'target_branch': 'dev', 'component': component.pk}]
        })
        self.assertFalse(feature_serializer.is_valid())
        self.assertTrue(len(feature_serializer.errors))

    def test_create_feature_when_component_non_existent(self):
        user = User.objects.create(username='user1')
        feature_serializer = FeatureSerializer(data={
            'name': 'feature1', 'status': Status.ACTIVE.value, 'description': 'new feature',
            'last_update_author': user.pk, 
            'changes': [{'source_branch': 'master', 'target_branch': 'dev', 'component': 55555}]
        })
        self.assertFalse(feature_serializer.is_valid())
        self.assertTrue(len(feature_serializer.errors))
    
    def test_create_feature(self):
        user = User.objects.create(username='user1')
        build_serializer = BuildSerializer(data={'name': 'new build', 'product': 'FCI2.0',
            'status': Status.PAUSE.value, 'property_templates': [
                {'name': 'name1', 'values': 'value1', 'status': Status.ACTIVE.value, 'kind': TemplateKind.FEATURE.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }},
                {'name': 'name2', 'values': 'value2', 'status': Status.ACTIVE.value, 'kind': TemplateKind.COMPONENT.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}
            ]})
        build_serializer.is_valid()
        new_build = build_serializer.save()
        component = Component.objects.create(repository='https://git1.ext.com/group/project',
            build=new_build, main_branch='master', status=Status.ACTIVE.value)
        feature_serializer = FeatureSerializer(data={
            'name': 'feature1', 'status': Status.ACTIVE.value, 'description': 'new feature',
            'last_update_author': user.pk, 
            'build': new_build.pk,
            'properties': [{'name': 'category1', 'value': 'value1', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}],
            'changes': [{'component': component.pk, 'properties': []}]
        })
        self.assertTrue(feature_serializer.is_valid(), f'Errors: {feature_serializer.errors}')
        saved_feature = feature_serializer.save()
        found_feature = Feature.objects.get(pk=saved_feature.pk)
        self.assertEqual(found_feature.name, 'feature1')
        self.assertEqual(found_feature.status, Status.ACTIVE.value)
        self.assertEqual(found_feature.description, 'new feature')
        self.assertEqual(found_feature.last_update_author.pk, user.pk)
        found_properties = Property.objects.filter(feature=found_feature)
        self.assertEqual(found_properties.count(), 1)
        self.assertListEqual(['category1', 'value1'], [found_properties.get().name, found_properties.get().value])
        found_changes = ComponentChange.objects.filter(feature=found_feature, component=component)
        self.assertEqual(found_changes.count(), 1)
        self.assertListEqual(['feature1', 'master', 'https://git1.ext.com/group/project'], [
            found_changes.get().source_branch, found_changes.get().target_branch, 
            found_changes.get().component.repository
        ])

    def test_update_feature(self):
        user = User.objects.create(username='user')
        user1 = User.objects.create(username='user1')
        build_serializer = BuildSerializer(data={'name': 'new build', 'product': 'FCI2.0',
            'status': Status.PAUSE.value, 'property_templates': [
                {'name': 'name1', 'values': 'value1', 'status': Status.ACTIVE.value, 'kind': TemplateKind.FEATURE.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }},
                {'name': 'name2', 'values': 'value2', 'status': Status.ACTIVE.value, 'kind': TemplateKind.COMPONENT.name, 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}
            ]})
        build_serializer.is_valid()
        new_build = build_serializer.save()
        component = Component.objects.create(build=new_build, repository='https://git1.ext.com/group/project',
            status=Status.ACTIVE.value, main_branch='master')
        component1 = Component.objects.create(build=new_build,repository='https://git1.ext.com/group/project1',
            status=Status.ACTIVE.value, main_branch='master')
        feature = Feature.objects.create(name='feature', status=Status.WIP.value, 
            description='new feature', last_update_author=user, build=new_build)
        Property.objects.create(feature=feature, name='main_branch', value='master')
        component_change = ComponentChange.objects.create(feature=feature, component=component1, 
            source_branch='my-local-branch', target_branch='branch-dev')
        Property.objects.create(component_change=component_change, name='release_name', value='some_release')
        feature_serializer = FeatureSerializer(feature, data={
            'name': 'update-feature1', 'status': Status.ACTIVE.value, 'description': 'update feature',
            'last_update_author': user1.pk, 
            'build': new_build.pk,
            'properties': [{'name': 'category1', 'value': 'value1', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}],
            'changes': [{
                'component': component.pk,
                'properties': [{'name': 'release_name', 'value': 'value1', 'style': {
                    'widget': 'select', 'read_only': False, 'hidden': False
                }}]}],
        })
        self.assertTrue(feature_serializer.is_valid(), f'Errors: {feature_serializer.errors}')
        saved_feature = feature_serializer.save()
        self.assertEqual(feature.pk, saved_feature.pk)
        found_feature = Feature.objects.get(pk=saved_feature.pk)
        self.assertEqual(found_feature.name, 'update-feature1')
        self.assertEqual(found_feature.status, Status.ACTIVE.value)
        self.assertEqual(found_feature.description, 'update feature')
        self.assertEqual(found_feature.last_update_author.pk, user1.pk)
        found_properties = Property.objects.filter(feature=found_feature)
        self.assertEqual(found_properties.count(), 1)
        self.assertListEqual(['category1', 'value1'], [found_properties.get().name, found_properties.get().value])
        found_changes = ComponentChange.objects.filter(feature=found_feature, component=component)
        self.assertEqual(found_changes.count(), 1)
        self.assertListEqual(['update-feature1', 'master', 'https://git1.ext.com/group/project'], [
            found_changes.get().source_branch, found_changes.get().target_branch, 
            found_changes.get().component.repository
        ])
        found_component_change_properties = Property.objects.filter(component_change=found_changes.get())
        self.assertEqual(found_component_change_properties.count(), 1)
        self.assertListEqual(['release_name', 'value1'], 
            [found_component_change_properties.get().name, found_component_change_properties.get().value])
