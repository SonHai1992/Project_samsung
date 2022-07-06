from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from database.models import Cadcam


# Create your views here.

@login_required
def view_cam_result(request):
    list_group = request.user.groups.all().values_list('name', flat=True)
    if "cad" in list_group:
        return render(request, 'CAM/cam-results.html')
    else:
        return HttpResponse("Ban khong co quyen truy cap")


@login_required
def cam_up_load(request):
    if request.method == "POST":
        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')
        created_by = request.user.username

        new_record = Cadcam(model=model,
                            process=process,
                            version=version,
                            pg_name=pg_name,
                            type="Cadcam",
                            created_by=created_by)
        new_record.save()
        return render(request, 'CAM/cam-upload.html', {'messages': 'uploaded successfully'})
    return render(request, 'CAM/cam-upload.html')
