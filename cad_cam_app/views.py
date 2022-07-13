from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import  datetime
from database.models import Cadcam, PROCESS_OPTIONS


# Create your views here.
@login_required
def index(request):
    custom =Cadcam.objects.filter(deleted=False,type='Cadcam')
    paginator = Paginator(custom,8)
    pageNumber = request.GET.get('page')
    customers = paginator.get_page(pageNumber)
    return render(request, 'CAM/index.html', {'customers': customers})


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
    custom =Cadcam.objects.filter(deleted=False)
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
        return render(request,'CAM/cam-upload.html', {'img': new_record.img,'messages': 'uploaded successfully'})
    return render(request, 'CAM/cam-upload.html', {"custom": custom})

@login_required
def Updateimg(request, id_input):
    updatefile =Cadcam.objects.get(id=id_input)
    if request.method == "POST":
        update_new = request.FILES['img']
        if updatefile.img != update_new:
            updatefile.img = update_new
            updatefile.save()
            return redirect('CAM/cam-upload.html.html')
    return render(request,'CAM/update_cam.html', {'updatefile': updatefile})

@login_required
def Delete(request,id_input):
    list_delete =Cadcam.objects.get(id=id_input)
    if request.method == "POST":
        list_delete.deleted = True
        list_delete.save()
    return redirect('index')

def Edit_upload(request,id_input):
    edit_file =Cadcam.objects.get(id=id_input)
    if request.method == "POST":
        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')
        img = request.FILES['img']
        created_by = request.user.username
        edit_file.model = model
        edit_file.process = process
        edit_file.version = version
        edit_file.pg_name = pg_name
        edit_file.img = img
        edit_file.modified_at = datetime.datetime.now()
        edit_file.modified_by = created_by
        edit_file.save()
        return redirect('index')
    return render(request, 'CAM/edit_cam.html', {'edit_file': edit_file, "p_o": PROCESS_OPTIONS})




