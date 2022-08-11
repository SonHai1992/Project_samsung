from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from database.models import Cadcam, PROCESS_OPTIONS, ORDER_STATUS, Images_cam, Images_pqc
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.db.models import Q


# Create your views here.


@login_required
def index(request):
    custom = Cadcam.objects.filter(deleted=False, status='Waiting').order_by('created_at')
    paginator = Paginator(custom, 10)
    pageNumber = request.GET.get('page')
    customers = paginator.get_page(pageNumber)
    return render(request, 'PQC/index.html', {'customers': customers})


@login_required
def comfirm_pqc(request, id_input):
    comfirm = Cadcam.objects.get(id=id_input)
    img_cam = Images_cam.objects.filter(name=comfirm)
    list_img_cam = img_cam.values_list("img_cam", flat=True)
    img_confrim = Images_pqc.objects.filter(name=comfirm)
    if request.method == "POST":
        my_status = request.POST.get('status')
        myimg_pqc = request.FILES.getlist('pqc_img')
        my_file = request.FILES.get('myImg')
        modified_by_pqc = request.user.username
        reason = request.POST.get('reason')

        comfirm.status = my_status
        comfirm.file_pqc = my_file
        comfirm.pqc_confirm_by = modified_by_pqc
        comfirm.type = "PQC"
        comfirm.reason = reason
        comfirm.pqc_confirm_at = datetime.datetime.now()
        comfirm.save()
        b = []
        for image in myimg_pqc:
            new_img = Images_pqc(name=comfirm, img_pqc=image)
            new_img.save()
            b.append(new_img.img_pqc.name)
        return redirect('index_pqc')
    return render(request, 'PQC/comfirm_pqc.html',
                  {'comfirm': comfirm, 'img_confrim': img_confrim, 'list_img_cam': list_img_cam,
                   'ORDER_STATUS': ORDER_STATUS})


@login_required
def Search_pqc(request):
    search = request.GET.get('search_pqc', '')
    pageNumber = request.GET.get('page')
    custom = Cadcam.objects.filter(
        Q(model__icontains=search) | Q(process__icontains=search) | Q(version__icontains=search), status='Waiting',
        deleted=False)
    paginator = Paginator(custom, 10)
    customers = paginator.get_page(pageNumber)
    return render(request, 'PQC/search_pqc.html', {'search': search, 'customers': customers})
