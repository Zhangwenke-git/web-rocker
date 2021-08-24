from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(TestSuit)
admin.site.register(TestCase)
admin.site.register(Scenario)
admin.site.register(Templates)


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_all_publish",)
    list_per_page = 3
    list_filter = ("name", "pub",)
    search_fields = ("name", "pub__name",)

    def show_all_publish(self, obj):  # ��Զ��ϵ��ʱ����list_displayչʾ֮��
        return [a.name for a in obj.pub.all()]


class PublishAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_per_page = 3
    list_filter = ("name",)
    search_fields = ("name",)



