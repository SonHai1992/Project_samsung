from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def view_cam_file(request):
    return render(request, 'PQC/pqc-results.html')


@login_required
def pqc_up_load(request):
    return render(request, 'PQC/pqc-upload.html')