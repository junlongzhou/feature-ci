from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from features import views

urlpatterns = [
    re_path(r'^(?P<version>(v1))/auth/$', views.user_auth),
    re_path(r'^(?P<version>(v1))/features/(?P<feature_id>[0-9]+)/commands/?$', views.FeatureCommand.as_view()),
    re_path(r'^(?P<version>(v1))/features/(?P<pk>[0-9]+)/?$', views.FeatureDetail.as_view()),
    re_path(r'^(?P<version>(v1))/features/[A-Za-z_-]+(?P<pk>[0-9]+)/?$', views.FeatureDetail.as_view()),
    re_path(r'^(?P<version>(v1))/features/(?P<slug>[\w-]*)$', views.FeatureList.as_view()),
    re_path(r'^(?P<version>(v1))/components/(?P<pk>[0-9]+)/?$', views.ComponentDetail.as_view()),
    re_path(r'^(?P<version>(v1))/components/(?P<slug>[\w-]*)$', views.ComponentList.as_view()),
    re_path(r'^(?P<version>(v1))/builds/(?P<pk>[0-9]+)/?$', views.BuildDetail.as_view()),
    re_path(r'^(?P<version>(v1))/builds/(?P<slug>[\w-]*)$', views.BuildList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
