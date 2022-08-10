# from django.contrib import admin
#
# # Register your models here.
# from database.models import Cadcam, Images
#
#
# class CadcamAdmin(admin.ModelAdmin):
#     list_display = ('id', 'model', 'process',
#                     'version', 'pg_name','file_cam','file_pqc',
#                     'status','reason'
#                     ,'type','deleted', 'created_at', 'created_by',
#                     'modified_at', 'modified_by','pqc_confirm_by',"pqc_confirm_at")
#     list_filter = ['model']
#
#
# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "img_cam", "img_pqc",'deleted','created_at','created_by','modified_at')
#
#
# admin.site.register(Cadcam, CadcamAdmin)
# admin.site.register(Images, ImagesAdmin)