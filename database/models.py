from django.db import models

# Create your models here.

PROCESS_OPTIONS = [(f'CNC{i}', f'CNC{i}') for i in range(3, 10)]


class Cadcam(models.Model):
    model = models.CharField(max_length=200)
    process = models.CharField(max_length=50, choices=PROCESS_OPTIONS)
    version = models.CharField(max_length=50)
    pg_name = models.CharField(max_length=100)
    img = models.ImageField(null=True, blank=True, upload_to='CAD_CAM/%Y/%m/%d/')
    pqc_img = models.ImageField(null=True, blank=True, upload_to='PQC/%Y/%m/%d/')
    status = models.CharField(max_length=50,default='Waiting')
    reason = models.CharField(max_length=1000,null=True, blank=True)
    type = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=200)

    def get_image_name(self):
        limit_character = 5
        main_name = self.img.name.split('/')[-1]  # => "abcdefgh.jpg"
        name_split = main_name.split('.')  # => ["abcdefgh", "jpg"]
        new_name = name_split[0][:limit_character]
        if len(name_split[0]) <= limit_character:
            return f"{new_name}.{name_split[-1]}"
        else:
            return f"{new_name}[...].{name_split[-1]}"
