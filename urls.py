from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_mlds/', include('django_mlds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^output', 'django_mlds.acefs.views.output'),
    (r'^secret-back-door', 'django_mlds.acefs.views.backdoor'),
    (r'^visitors', 'django_mlds.acefs.views.visitors'),
    (r'^visitor_list/(?P<page_num>[0-9]*)', 'django_mlds.acefs.views.visitor_list'),
    (r'^visitor_detail/(?P<visitor_id>[0-9]*)', 'django_mlds.acefs.views.visitor_detail'),
        (r'^', 'django_mlds.acefs.views.main'),
    )
