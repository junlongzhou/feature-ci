from django.db import models
from django.contrib.auth.models import User
from features.constants import Status, MAXIMUM_LEN_OF_GIT_BRANCH, TemplateKind

class Build(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    status = models.SmallIntegerField(default=Status.ACTIVE.value)
    product = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)

    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'{self.product} {self.name}'

    @property
    def property_templates(self):
        self._property_templates = PropertyTemplate.objects.filter(build=self)
        return self._property_templates
    
    @property_templates.setter
    def property_templates(self, value):
        self._property_templates = value

class Feature(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    status = models.SmallIntegerField(default=Status.ACTIVE.value)
    description = models.TextField(blank=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_update_author = models.ForeignKey(User, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    @property
    def properties(self):
        self._properties = Property.objects.filter(feature=self)
        return self._properties
    
    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def changes(self):
        self._changes = ComponentChange.objects.filter(feature=self)
        return self._changes
    
    @changes.setter
    def changes(self, value):
        self._changes = value

class Component(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.SmallIntegerField(default=Status.ACTIVE.value)
    repository = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    main_branch = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    build = models.ForeignKey(Build, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    @property
    def properties(self):
        self._properties = Property.objects.filter(component=self)
        return self._properties
    
    @properties.setter
    def properties(self, value):
        self._properties = value

class ComponentChange(models.Model):
    id = models.BigAutoField(primary_key=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    target_branch = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    source_branch = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)

    class Meta:
        ordering = ['-id']
        unique_together = ['feature', 'component']

    @property
    def properties(self):
        self._properties = Property.objects.filter(component_change=self)
        return self._properties
    
    @properties.setter
    def properties(self, value):
        self._properties = value

class PropertyTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, null=True)
    kind = models.CharField(max_length=100, choices=TemplateKind.to_choices(), null=True)
    name = models.CharField(max_length=MAXIMUM_LEN_OF_GIT_BRANCH)
    values = models.CharField(max_length=500)
    status = models.SmallIntegerField(default=Status.ACTIVE.value)
    style = models.CharField(max_length=250, default='widget:text;read_only:false;hidden:false;')

    class Meta:
        ordering = ['-id']
        unique_together = ['build', 'name']

class Property(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=500)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    component_change = models.ForeignKey(ComponentChange, on_delete=models.CASCADE, null=True)
    style = models.CharField(max_length=250, default='widget:text;read_only:false;hidden:false;')

    class Meta:
        ordering = ['-id']
