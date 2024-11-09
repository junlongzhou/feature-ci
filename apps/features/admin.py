from typing import Any
from django.contrib import admin
from features.models import Build, PropertyTemplate, Component, Property
from features.constants import TemplateKind

class PropertyTemplateInline(admin.TabularInline):
    model = PropertyTemplate
    fields = ['name', 'values', 'kind']

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    exclude = ['status']
    inlines = [
        PropertyTemplateInline,
    ]
    list_display = ['name', 'product']

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    exclude = ['status']
    list_display = ['repository', 'main_branch']
    change_form_template = 'component_change_form.html'
    
    def changeform_view(self, request, object_id, form_url, extra_context):
        if not extra_context:
            extra_context = {
                'build_property_templates': {},
                'current_build_id': '',
                'component_properties': []
            }
        build_property_templates = {}
        for build in Build.objects.all():
            build_property_templates[build.pk] = []
            for build_property_template in build.property_templates:
                if build_property_template.kind == TemplateKind.COMPONENT.name:  
                    build_property_templates[build.pk].append({
                        'id': build_property_template.pk,
                        'name': build_property_template.name,
                        'value': build_property_template.values
                    })
        extra_context['build_property_templates'] = build_property_templates
        if object_id:
            component_properties = []
            instance = Component.objects.get(pk=object_id)
            extra_context['current_build_id'] = instance.build.pk
            for component_property in instance.properties:
                component_properties.append({
                    'id': component_property.pk,
                    'name': component_property.name,
                    'value': component_property.value
                })
            extra_context['component_properties'] = component_properties
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        property_map = {}
        for param_name, param_value in request.POST.items():
            param_name_splits = param_name.split('-property-')
            if param_name.startswith('form-') and len(param_name_splits)==2:
                property_id, field_name = param_name_splits[0].lstrip('form-'), param_name_splits[1]
                if property_id not in property_map:
                    property_map[property_id] = {}
                property_map[property_id][field_name] = param_value
        changed_properties = []
        for values in property_map.values():
            changed_properties.append(Property(component=obj, **values))
        Property.objects.filter(component=obj).delete()
        Property.objects.bulk_create(changed_properties)
