from django.contrib import admin
from django_mlds.flatblocks.models import FlatBlock
 
class FlatBlockAdmin(admin.ModelAdmin):
    ordering = ['slug',]
    list_display = ('slug', 'content')
    search_fields = ('slug', 'header', 'content')

admin.site.register(FlatBlock, FlatBlockAdmin)
