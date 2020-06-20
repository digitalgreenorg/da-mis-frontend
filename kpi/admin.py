# coding: utf-8
from django.contrib import admin

from hub.models import ExtraUserDetail
from .models import AuthorizedApplication
from .models import LocationAccess
from .models.geography import LocationAccessAdmin

# Register your models here.
admin.site.register(AuthorizedApplication)
admin.site.register(ExtraUserDetail)
admin.site.register(LocationAccess, LocationAccessAdmin)
admin.site.site_header = 'DA/SMS Administration'
admin.site.site_title = 'Admin'
admin.site.index_title = 'DA/SMS'
