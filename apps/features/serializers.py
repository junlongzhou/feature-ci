from os import environ
from dataclasses import dataclass, field
from features.models import Feature, Component, Build, ComponentChange, \
    PropertyTemplate, Property
from features.constants import Status, FCI_ID_PREFIX, FCI_ID_MAXIMUM_LEN, \
    MAXIMUM_LEN_OF_GIT_BRANCH, Action, Widget
from rest_framework import serializers
from features.utils import unique_fci_id
from features.signals import feature_save, post_feature_command
from utils.git import parse_repo_path

FEATURE_APPROVE_STATUS = environ.get('FEATURE_APPROVE_STATUS', Status.WIP.name)
FEATURE_ABANDON_STATUS = environ.get('FEATURE_ABANDON_STATUS', Status.ABANDONED.name)
GERRIT_URL = environ.get('GERRIT_URL', '')
GERRIT_REPO = environ.get('GERRIT_REPO', '')

@dataclass
class Style:
    widget: str
    read_only: bool = False
    hidden: bool = False
    command: str = ''
    values: str = ''

    def __str__(self) -> str:
        return f'widget:{self.widget};read_only:{str(self.read_only).lower()};hidden:{str(self.hidden).lower()};command:{self.command};values:{self.values };'

class StyleField(serializers.Field):

    def to_internal_value(self, data):
        if isinstance(data, str):
            return data
        if 'widget' not in data:
            raise serializers.ValidationError('Field widget is required.')
        if data.get('widget') not in Widget.values():
            raise serializers.ValidationError(f'Incorrect widget. Expected a value from {Widget.to_choices()}')
        return str(Style(data.pop('widget'), **data))
    
    def to_representation(self, value):
        if isinstance(value, str):
            dict_value = {}
            for value_split in value.split(';'):
                splits = value_split.split(':')
                if len(splits) == 2:
                    converted_value = splits[1].strip()
                    if converted_value.lower() in ['false', 'true']:
                        converted_value = converted_value == 'true'
                    dict_value[splits[0].strip()] = converted_value
            return dict_value
        return value

class PropertySerializer(serializers.ModelSerializer):
    style = StyleField()

    class Meta:
        model = Property
        fields = ['id', 'name', 'value', 'style']

    def to_internal_value(self, data):
        if isinstance(data.get('status'), str):
            data['status'] = Status[data.get('status')].value
        return super().to_internal_value(data)
    
    def save(self, **kwargs):
        queryset = Property.objects.filter(
            name=self.validated_data.get('name', ''), **kwargs)
        if queryset.exists():
            existing_property = queryset[0]
            existing_property.value = self.validated_data.get('value', existing_property.value)
            existing_property.style = self.validated_data.get('style', existing_property.style)
            existing_property.save()
            return existing_property
        return Property.objects.create(**kwargs, **self.validated_data)
    
    @classmethod
    def bulk_save(cls, properties, **kwargs):
        saved_properties = []
        for property in properties:
            serializer = PropertySerializer(data=property)
            serializer.is_valid(raise_exception=True)
            saved_properties.append(serializer.save(**kwargs))
        return saved_properties
    
    @classmethod
    def bulk_delete(cls, properties, **kwargs):
        properties_names = [property.get('name', '') for property in properties]
        Property.objects.filter(**kwargs).exclude(name__in=properties_names).delete()

class ComponentSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True)

    class Meta:
        model = Component
        fields = ['id', 'repository', 'main_branch', 'build',  'status', 'properties']

    def to_internal_value(self, data):
        if isinstance(data.get('status'), str):
            data['status'] = Status[data.get('status')].value
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = Status(representation['status']).name
        representation['display_name'] = parse_repo_path(instance.repository)
        return representation

    def create(self, validated_data):
        properties = validated_data.pop('properties', [])
        new_component = Component.objects.create(**validated_data)
        new_component.properties = PropertySerializer.bulk_save(properties, component=new_component)
        return new_component
    
    def update(self, instance, validated_data):
        properties = validated_data.pop('properties', [])
        instance.repository = validated_data.get('repository', instance.repository)
        instance.build = validated_data.get('build', instance.build)
        instance.main_branch = validated_data.get('main_branch', instance.main_branch)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        PropertySerializer.bulk_delete(properties, component=instance)
        instance.properties = PropertySerializer.bulk_save(properties, component=instance)
        return instance

class ComponentChangeSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, required=False)
    target_branch = serializers.CharField(required=False, max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    source_branch = serializers.CharField(required=False, max_length=MAXIMUM_LEN_OF_GIT_BRANCH)

    class Meta:
        model = ComponentChange
        fields = ['id', 'target_branch', 'source_branch', 'properties', 'component']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['repository'] = instance.component.repository
        representation['display_name'] = parse_repo_path(instance.component.repository)
        return representation
        
    def save(self, feature=None):
        component = self.validated_data.pop('component')
        existing_changes = ComponentChange.objects.filter(feature=feature, component=component)
        properties = self.validated_data.pop('properties', [])
        if existing_changes:
            existing_change = existing_changes.get()
            existing_change.target_branch = self.validated_data.get('target_branch',
                existing_change.target_branch)
            existing_change.source_branch = self.validated_data.get('source_branch',
                existing_change.source_branch)
            existing_change.save()
            PropertySerializer.bulk_delete(properties, component_change=existing_change)
            existing_change.properties = PropertySerializer.bulk_save(properties, component_change=existing_change)
            return existing_change
        else:
            new_component_change = ComponentChange.objects.create(feature=feature,
                component=component, **self.validated_data)
            new_component_change.properties = PropertySerializer.bulk_save(properties, component_change=new_component_change)
            return new_component_change

    @classmethod
    def bulk_save(cls, changes, feature):
        saved_changes = []
        ComponentChange.objects.filter(feature=feature).exclude(
            component__in=[ change['component'] for change in changes]).delete()
        for change in changes:
            if not change.get('target_branch', None):
                change['target_branch'] = change['component'].main_branch
            if not change.get('source_branch', None):
                change['source_branch'] = feature.name
            change['component'] = change['component'].pk
            serializer = ComponentChangeSerializer(data=change)
            serializer.is_valid(raise_exception=True)
            saved_changes.append(serializer.save(feature=feature))
        return saved_changes

class FeatureSerializer(serializers.ModelSerializer):
    changes = ComponentChangeSerializer(many=True)
    properties = PropertySerializer(many=True)

    class Meta:
        model = Feature
        fields = ['id', 'name', 'status', 'description', 'changes',
            'last_update_date', 'last_update_author', 'properties', 'build']
        extra_kwargs = {
            'action': {'write_only': True, 'required': False}
        }
    
    def to_internal_value(self, data):
        action = data.get('action', '').lower()
        if isinstance(data.get('status'), str):
            data['status'] = Status[data.get('status')].value
        if action == Action.APPROVE.value and self.instance:
            data['status'] = Status[FEATURE_APPROVE_STATUS].value
        elif action == Action.ABANDON.value and self.instance:
            data['status'] = Status[FEATURE_ABANDON_STATUS].value
        return super().to_internal_value(data)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['last_update_author'] = instance.last_update_author.username
        representation['status'] = Status(representation['status']).name
        display_id = unique_fci_id(FCI_ID_PREFIX, instance.id, FCI_ID_MAXIMUM_LEN)
        representation['display_id'] = display_id
        representation['change_json'] = f'{GERRIT_URL}/q/project:{GERRIT_REPO}+subject:"{display_id}: {representation["name"]}"'
        return representation
        
    def validate_changes(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(f'Changes must be a non-empty list: {value}')
        return value
    
    def validate_properties(self, value):
        if not value or not isinstance(value, list):
            raise serializers.ValidationError(f'Properties must be a non-empty list: {value}')
        return value
        
    def create(self, validated_data):
        changes = validated_data.pop('changes')
        properties = validated_data.pop('properties')
        feature = Feature.objects.create(**validated_data)
        feature.changes = ComponentChangeSerializer.bulk_save(changes, feature)
        feature.properties = PropertySerializer.bulk_save(properties, feature=feature)
        return feature

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.last_update_author = validated_data.get('last_update_author', instance.last_update_author)
        instance.build = validated_data.get('build', instance.build)
        instance.save()
        changes = validated_data.pop('changes', None)
        if changes:
            instance.changes = ComponentChangeSerializer.bulk_save(changes, instance)
        properties = validated_data.pop('properties', None)
        if properties:
            PropertySerializer.bulk_delete(properties, feature=instance)
            instance.properties = PropertySerializer.bulk_save(properties, feature=instance)
        return instance
    
    def save(self, **kwargs):
        saved_instance = super().save(**kwargs)
        feature_save.send(Feature.__class__, data=FeaturePrettySerializer(saved_instance).data)
        return saved_instance
    
class PropertyTemplateSerializer(serializers.ModelSerializer):
    style = StyleField()

    class Meta:
        model = PropertyTemplate
        fields = ['id', 'kind', 'name', 'values', 'status', 'style']

    def to_internal_value(self, data):
        if isinstance(data.get('status'), str):
            data['status'] = Status[data.get('status')].value
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = Status(representation['status']).name
        return representation

    @classmethod
    def bulk_save(cls, property_templates, build):
        saved_property_templates = []
        for property_template in property_templates:
            queryset = PropertyTemplate.objects.filter(build=build, name=property_template.get('name', ''))
            if queryset.exists():
                existing_property_template = queryset.get()
                existing_property_template.kind = property_template.get('kind', existing_property_template.kind)
                existing_property_template.name = property_template.get('name', existing_property_template.name)
                existing_property_template.values = property_template.get('values', existing_property_template.values)
                existing_property_template.style = property_template.get('style', existing_property_template.style)
                existing_property_template.save()
                saved_property_templates.append(existing_property_template)   
            else:
                saved_property_templates.append(
                    PropertyTemplate.objects.create(build=build, **property_template))
        return saved_property_templates
    
    @classmethod
    def bulk_delete(cls, exclude_property_templates, build):
        property_template_names = [property_template.get('name', '') 
            for property_template in exclude_property_templates]
        PropertyTemplate.objects.filter(build=build).exclude(name__in=property_template_names).delete()

class BuildSerializer(serializers.ModelSerializer):
    property_templates = PropertyTemplateSerializer(many=True)

    class Meta:
        model = Build
        fields = ['id', 'name', 'product', 'status', 'property_templates']
    
    def to_internal_value(self, data):
        if isinstance(data.get('status'), str):
            data['status'] = Status[data.get('status')].value
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = Status(representation['status']).name
        return representation

    def create(self, validated_data):
        property_templates = validated_data.pop('property_templates', [])
        new_build = Build.objects.create(**validated_data)
        new_build.property_templates = PropertyTemplateSerializer.bulk_save(property_templates, new_build)
        return new_build

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.product = validated_data.get('product', instance.product)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        property_templates = validated_data.pop('property_templates', [])
        PropertyTemplateSerializer.bulk_delete(property_templates, instance)
        instance.property_templates = PropertyTemplateSerializer.bulk_save(property_templates, instance)
        return instance

class FeaturePrettySerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ['id', 'name', 'status', 'description', 'changes',
            'last_update_date', 'last_update_author', 'properties']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('properties')
        representation.pop('changes')
        representation['id'] = unique_fci_id(FCI_ID_PREFIX, instance.id, FCI_ID_MAXIMUM_LEN)
        representation['last_update_author'] = instance.last_update_author.username
        representation['status'] = Status(representation['status']).name
        for property_item in instance.properties:
            representation[property_item.name] = property_item.value
        formatted_changes = []
        for change in instance.changes:
            formatted_change = {
                'repository': change.component.repository,
                'target_branch': change.target_branch,
                'source_branch': change.source_branch
            }
            for property_item in change.component.properties:
                formatted_change[property_item.name] = property_item.value
            for property_item in change.properties:
                formatted_change[property_item.name] = property_item.value
            formatted_changes.append(formatted_change)
        representation['changes'] = formatted_changes 
        return representation

class FeatureCommandSerializer(serializers.Serializer):
    feature_id = serializers.IntegerField()
    command_name = serializers.CharField(max_length=200, trim_whitespace=True)
    command_args = serializers.JSONField(default={}, required=False)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        results = post_feature_command.send(FeatureCommandSerializer.__class__, 
            feature_id=unique_fci_id(FCI_ID_PREFIX, validated_data.get('feature_id'), FCI_ID_MAXIMUM_LEN), 
            command_name=validated_data.get('command_name'),
            command_args=validated_data.get('command_args')
        )
        validated_data['message'] = results[-1][-1] if results and results[-1] else ''
        return {**validated_data}
