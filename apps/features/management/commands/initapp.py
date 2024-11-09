from django.core.management.base import BaseCommand
from features.models import Component, Build, Property, PropertyTemplate
from features.constants import TemplateKind

class Command(BaseCommand):
    help = 'Create default example data for app'

    def add_arguments(self, parser):
        parser.add_argument('--repository', type=str)
        parser.add_argument('--build', type=str)
        parser.add_argument('--product', type=str)

    def handle(self, *args, **options):
        repository = options['repository']
        build = options['build']
        product = options['product']
        new_build = None
        if not Build.objects.filter(name=build).exists():
            new_build = Build.objects.create(name=build, product=product)
            PropertyTemplate.objects.create(name='release_notes', values='feature,pronto,interface_change', style='widget:select;read_only:false;hidden:false;values:feature,pronto,interface_change;', build=new_build, kind=TemplateKind.FEATURE.name)
            PropertyTemplate.objects.create(name='need_tag', values='true,false', style='widget:select;read_only:false;hidden:false;values:true,false;', build=new_build, kind=TemplateKind.COMPONENT.name)
            PropertyTemplate.objects.create(name='tag_level', values='no tag,major,minor,patch', style='widget:select;read_only:false;hidden:false;values:no tag,major,minor,patch;', build=new_build, kind=TemplateKind.COMPONENT.name)
        else:
            new_build = Build.objects.filter(name=build).get()
        if not Component.objects.filter(repository=repository).exists():
            new_component = Component.objects.create(repository=repository, main_branch='master', build=new_build)
            Property.objects.create(component=new_component, name='need_tag', value='true', style='widget:select;read_only:false;hidden:false;values:true,false;')
            Property.objects.create(component=new_component, name='tag_level', value='no tag', style='widget:select;read_only:false;hidden:false;values:no tag,major,minor,patch;')
