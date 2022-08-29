from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from database.models import Cadcam, PROCESS_OPTIONS, Images_cam, Images_pqc
from django.contrib.auth.models import User
import xlwt
from PIL import Image
from django.db.models import Q
import os
from project.settings import BASE_DIR
import re


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
    list_img_cam = Images_cam.objects.filter(name=list_view)
    list_img_pqc = Images_pqc.objects.filter(name=list_view)
    img_cam_list = list_img_cam.values_list("img_cam", flat=True)
    img_pqc_list = list_img_pqc.values_list("img_pqc", flat=True)
    return render(request, 'CAM/cam_view.html',
                  {'list_view': list_view, 'img_cam_list': img_cam_list, 'img_pqc_list': img_pqc_list,
                   "PROCESS_OPTIONS": PROCESS_OPTIONS,
                   "id_input": id_input})


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
        if (model and process and version and pg_name):
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
                new_img = Images_cam(name=new_record,
                                     img_cam=image
                                     )
                new_img.save()
                a.append(new_img.img_cam.name)
        return redirect("cam_upload")
    return render(request, 'CAM/cam-upload.html',
                  {"custom": custom, "PROCESS_OPTIONS": PROCESS_OPTIONS, 'messages': ''})


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

    # delete database
    img_cam = Images_cam.objects.filter(name=edit_file)

    old_id = img_cam.values_list('id', flat=True)
    old_id_copy = list(old_id).copy()
    # delete file local
    list_cam_img = img_cam.values_list('img_cam', flat=True)

    if request.method == "POST":
        # except Exception as e:
        #     print(e)

        old_excel_file = edit_file.file_cam

        model = request.POST.get('model')
        process = request.POST.get('process')
        version = request.POST.get('version')
        pg_name = request.POST.get('pg_name')
        myfile_img = request.FILES.getlist('img')
        excel_file = request.FILES.get('excel')
        created_by = request.user.username
        edit_file.model = model
        edit_file.process = process
        edit_file.version = version
        edit_file.pg_name = pg_name
        if excel_file:
            edit_file.file_cam = excel_file
        edit_file.modified_at = datetime.datetime.now()
        edit_file.modified_by = created_by
        edit_file.save()

        for image in myfile_img:
            new_img = Images_cam(name=edit_file,
                                 img_cam=image
                                 )
            new_img.save()

        for i in Images_cam.objects.filter(id__in=list(old_id_copy)):
            try:
                os.remove(f"{BASE_DIR}/media/{i.img_cam}")
            except Exception as e:
                pass
            i.delete()

        if excel_file and old_excel_file:
            os.remove(f"{BASE_DIR}/media/{old_excel_file}")

        return redirect('index')
    return render(request, 'CAM/edit_cam.html',
                  {'edit_file': edit_file, 'list_cam_img': list_cam_img, "PROCESS_OPTIONS": PROCESS_OPTIONS})


@login_required
def Search(request):
    search = request.GET.get('search', '')
    # pageNumber = request.GET.get('page')
    custom = Cadcam.objects.filter(
        Q(model__icontains=search) | Q(process__icontains=search) | Q(version__icontains=search), deleted=False)
    # paginator = Paginator(custom, 10)
    # customers = paginator.get_page(pageNumber)
    return render(request, 'CAM/search.html', {'search': search, 'custom': custom})


@login_required
def export_users_xls(request, id_input):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Model')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['model', 'process', 'version', 'pg_name', 'pqc_confirm_by', 'pqc_confirm_at', 'reason', 'img_cam', 'img_pqc']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Cadcam.objects.filter(id=id_input)
    data = rows.values_list('model', 'process', 'version', 'pg_name', 'pqc_confirm_by',
                                                          'pqc_confirm_at', 'reason')
    rows_1 = Images_cam.objects.filter(name=rows[0]).values_list('img_cam', flat=True)
    rows_2 = Images_pqc.objects.filter(name=rows[0]).values_list('img_pqc', flat=True)
    for row in data:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    if rows_1:
        col_num += 1
        old_row = row_num
        for i in rows_1:
            img = Image.open("media/" + i)
            size = 300, 200
            img.thumbnail(size, Image.ANTIALIAS)
            r, g, b = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.save('imagetoadd.bmp')
            ws.insert_bitmap('imagetoadd.bmp', old_row, col_num)
            old_row += 1

    if rows_2:
        col_num += 1
        old_row = row_num
        for i in rows_2:
            img = Image.open("media/" + i)
            size = 300, 200
            img.thumbnail(size, Image.ANTIALIAS)
            r, g, b = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.save('imagetoadd.bmp')
            ws.insert_bitmap('imagetoadd.bmp', old_row, col_num)
            old_row += 1

    wb.save(response)

    return response



@login_required
def export_model_xls(request):
    search_old = re.findall("&search=(.+)$|&", request.headers['Referer'])
    search = search_old[0].replace("+", " ")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Model')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['model', 'process', 'version', 'pg_name', 'pqc_confirm_by', 'pqc_confirm_at', 'reason', 'img_cam', 'img_pqc']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Cadcam.objects.filter(model=search)
    data_all = rows.values_list('model', 'process', 'version', 'pg_name', 'pqc_confirm_by',
                        'pqc_confirm_at', 'reason')

    for idx, model in enumerate(rows):
        row_num += 1
        data = data_all[idx]
        rows_1 = Images_cam.objects.filter(name=model).values_list('img_cam', flat=True)
        rows_2 = Images_pqc.objects.filter(name=model).values_list('img_pqc', flat=True)
        print(data)
        for col_num in range(len(data)):
            ws.write(row_num, col_num, str(data[col_num]), font_style)

        if rows_1:
            col_num += 1
            for i in rows_1:
                img = Image.open("media/" + i)
                size = 300, 200
                img.thumbnail(size, Image.ANTIALIAS)
                r, g, b = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.save('imagetoadd.bmp')
                ws.insert_bitmap('imagetoadd.bmp', row_num, col_num)


        if rows_2:
            col_num += 1
            for i in rows_2:
                img = Image.open("media/" + i)
                size = 300, 200
                img.thumbnail(size, Image.ANTIALIAS)
                r, g, b = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.save('imagetoadd.bmp')
                ws.insert_bitmap('imagetoadd.bmp', row_num, col_num)
    wb.save(response)

    return response
