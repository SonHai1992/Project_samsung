from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

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
    return render(request, 'CAM/cam-upload.html')