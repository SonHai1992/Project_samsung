from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from database.models import Cadcam, PROCESS_OPTIONS, ORDER_STATUS


# Create your views here.


@login_required
def index(request):
    custom =Cadcam.objects.filter(deleted=False, status='Waiting').order_by('created_at')
    paginator = Paginator(custom,8)
    pageNumber = request.GET.get('page')
    customers = paginator.get_page(pageNumber)
    return render(request, 'PQC/index.html', {'customers': customers})


@login_required
def comfirm_pqc(request,id_input):
    comfirm =Cadcam.objects.get(id=id_input)
    if request.method == "POST":
        status = request.POST.get('status')
        myfile_pqc = request.FILES['pqc_img']
        modified_by_pqc = request.user.username
        reason = request.POST.get('reason')

        comfirm.status = status
        comfirm.pqc_img = myfile_pqc
        comfirm.pqc_confirm_by = modified_by_pqc
        comfirm.reason = reason.strip()
        comfirm.pqc_confirm_at = datetime.datetime.now()
        comfirm.type = 'pqc'
        comfirm.save()
        return redirect('index_pqc')
    return render(request,'PQC/comfirm_pqc.html',{'comfirm': comfirm,'ORDER_STATUS': ORDER_STATUS})


@login_required
def Search_pqc(request):
    search = request.GET.get('search_pqc', '')
    pageNumber = request.GET.get('page')
    custom = Cadcam.objects.filter(model__icontains=search, status='Waiting', deleted=False)
    paginator = Paginator(custom, 8)
    customers = paginator.get_page(pageNumber)
    return render(request, 'PQC/search_pqc.html', {'search': search, 'customers': customers})
