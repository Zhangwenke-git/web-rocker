from django.contrib import admin

# Register your models here.
from public.models import *




admin.site.register(Role)
admin.site.register(FirstLayerMenu)
admin.site.register(UserProfile)