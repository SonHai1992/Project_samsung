from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from database.models import Cadcam, PROCESS_OPTIONS, Images
from django.contrib.auth.models import User
import xlwt
from PIL import Image


# Create your views here.
@login_required
def index(request):
    custom = Cadcam.objects.filter(deleted=False).order_by('-pqc_confirm_at')
    paginator = Paginator(custom, 10)
    pageNumber = request.GET.get('page')
    customers = paginator.get_page(pageNumber)
    return render(request, 'CAM/index.html', {'customers': customers})


@login_required
def view_pqc_result(request, id_input):
    list_view = Cadcam.objects.get(id=id_input)
    return render(request, 'CAM/cam_view.html',
                  {'list_view': list_view, "PROCESS_OPTIONS": PROCESS_OPTIONS, "id_input": id_input})


@login_required
def cam_up_load(request):
    custom = Cadcam.objects.filter(deleted=False)
    if request.method == "POST":
        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')
        myfile = request.FILES.getlist('img')
        excel = request.FILES.get('excel')
        created_by = request.user.username
        new_record = Cadcam(model=model,
                            process=process,
                            version=version,
                            pg_name=pg_name,
                            file_cam=excel,
                            type="Cadcam",
                            created_by=created_by
                            )
        new_record.save()
        a = []
        for image in myfile:
            new_img = Images(name=new_record,
                             img_cam=image
                             )
            new_img.save()
            a.append(new_img.img_cam.name)
        return render(request, 'CAM/cam-upload.html', {'img': a, 'messages': 'uploaded successfully'})
    return render(request, 'CAM/cam-upload.html', {"custom": custom, "PROCESS_OPTIONS": PROCESS_OPTIONS})


@login_required
def Delete(request, id_input):
    list_delete = Cadcam.objects.get(id=id_input)
    if request.method == "POST":
        list_delete.deleted = True
        list_delete.save()
    return redirect('index')


@login_required
def Edit_upload(request, id_input):
    edit_file = Cadcam.objects.get(id=id_input)
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
    return render(request, 'CAM/edit_cam.html', {'edit_file': edit_file, "PROCESS_OPTIONS": PROCESS_OPTIONS})


@login_required
def Search(request):
    search = request.GET.get('search', '')
    pageNumber = request.GET.get('page')
    custom = Cadcam.objects.filter(model__icontains=search, deleted=False)
    paginator = Paginator(custom, 8)
    customers = paginator.get_page(pageNumber)
    return render(request, 'CAM/search.html', {'search': search, 'customers': customers})


@login_required
def export_users_xls(request, id_input):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PQC result')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['model', 'process', 'version', 'pg_name', 'pqc_confirm_by', 'reason', 'img', 'pqc_img']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Cadcam.objects.filter(id=id_input).values_list('model', 'process', 'version', 'pg_name', 'pqc_confirm_by',
                                                          'reason', 'img', 'pqc_img')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in [len(row) - 1, len(row) - 2]:
                img = Image.open("media/" + row[col_num])
                size = 300, 200
                img.thumbnail(size, Image.ANTIALIAS)
                r, g, b = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.save('imagetoadd.bmp')
                ws.insert_bitmap('imagetoadd.bmp', row_num, col_num)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
