import datetime
import dateparser

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PROCESS_OPTIONS = [(f'CNC{i}', f'CNC{i}') for i in range(3, 10)]

ORDER_STATUS = [(0, 'OK'), (1, 'NG')]


def get_group_list(self):
    return list(self.groups.values_list('name', flat=True))


User.add_to_class('get_group_list', get_group_list)


class Cadcam(models.Model):
    model = models.CharField(max_length=200)
    process = models.CharField(max_length=50, choices=PROCESS_OPTIONS)
    version = models.CharField(max_length=50)
    pg_name = models.CharField(max_length=100)
    file_cam = models.FileField(null=True, blank=True, upload_to='CAD_CAM/FILES/%Y/%m/%d/')
    file_pqc = models.FileField(null=True, blank=True, upload_to='PQC/FILES/%Y/%m/%d/')
    status = models.CharField(max_length=50, default='Waiting')
    reason = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_at = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=200)
    pqc_confirm_by = models.CharField(max_length=200, null=True, blank=True)
    pqc_confirm_at = models.DateTimeField(null=True, blank=True)

    # class Meta:
    #     db_table = "CAM"

    def get_image_name(self):
        limit_character = 5
        main_name = self.img.name.split('/')[-1]  # => "abcdefgh.jpg"
        name_split = main_name.split('.')  # => ["abcdefgh", "jpg"]
        new_name = name_split[0][:limit_character]
        if len(name_split[0]) <= limit_character:
            return f"{new_name}.{name_split[-1]}"
        else:
            return f"{new_name}[...].{name_split[-1]}"

    def get_submit_day(self):
        return (datetime.datetime.now() - dateparser.parse(str(self.created_at).split(".")[0])).days


class Images_cam(models.Model):
    name = models.ForeignKey(Cadcam, on_delete=models.CASCADE)
    img_cam = models.ImageField(null=True, blank=True, upload_to='CAD_CAM/IMAGES/%Y/%m/%d/')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.CharField(null=True, blank=True, max_length=200)
    modified_at = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(null=True, blank=True, max_length=200)



class Images_pqc(models.Model):
    name = models.ForeignKey(Cadcam, on_delete=models.CASCADE)
    img_pqc = models.ImageField(null=True, blank=True, upload_to='PQC/IMAGES/%Y/%m/%d/')
    deleted = models.BooleanField(default=False)
    pqc_confirm_by = models.CharField(max_length=200, null=True, blank=True)
    pqc_confirm_at = models.DateTimeField(null=True, blank=True)