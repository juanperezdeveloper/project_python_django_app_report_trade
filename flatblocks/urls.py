from django.conf.urls.defaults import *
from django.contrib.admin.views.decorators import staff_member_required
from django_mlds.flatblocks.views import edit

urlpatterns = patterns('',
    url('^edit/(?P<pk>\d+)/$', staff_member_required(edit), name='flatblocks-edit')
)
