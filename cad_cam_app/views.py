from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from database.models import Cadcam


# Create your views here.

@login_required
def view_cam_result(request):
    list_model = list(set(Cadcam.objects.all().values_list('model', flat=True)))
    if request.method == "POST":
        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')

        result = Cadcam.objects.filter(
            model=model,
            process=process,
            version=version,
            pg_name=pg_name).first()
        if result:
            return render(request, 'CAM/cam-results.html', {'img': result.img, 'list_model': list_model})
        else:
            return render(request, 'CAM/cam-results.html', {'list_model': list_model, "message": "Item not found"})

    return render(request, 'CAM/cam-results.html', {'list_model': list_model})


@login_required
def cam_up_load(request):
    if request.method == "POST":
        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')
        myfile = request.FILES['img']
        created_by = request.user.username

        new_record = Cadcam(model=model,
                            process=process,
                            version=version,
                            pg_name=pg_name,
                            type="Cadcam",
                            created_by=created_by,
                            img=myfile
                            )
        new_record.save()
        return render(request, 'CAM/cam-upload.html', {'messages': 'uploaded successfully'})
    return render(request, 'CAM/cam-upload.html')
