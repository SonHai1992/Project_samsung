from django.contrib import admin

# Register your models here.
from database.models import Cadcam


class CadcamAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'process',
                    'version', 'pg_name', 'img', 'type',
                    'deleted', 'created_at', 'created_by',
                    'modified_at', 'modified_by')


admin.site.register(Cadcam,CadcamAdmin)