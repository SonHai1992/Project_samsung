from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from database.models import Cadcam, PROCESS_OPTIONS


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
        myfile_pqc = request.FILES['pqc_img']
        comfirm.pqc_img = myfile_pqc
        comfirm.save()
        return redirect('index_pqc')
    return render(request,'PQC/comfirm_pqc.html',{'comfirm': comfirm})

