from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.models import Cadcam


# Create your views here.

@login_required
def home_page(request):
    labels = list(set(list((Cadcam.objects.filter(deleted=False).values_list("model", flat=True)))))
    labels.sort()
    print(labels)

    data1 = []
    data2 = []
    data3 = []
    for i in labels:

        ok = Cadcam.objects.filter(model=i, deleted=False, status="OK")
        ng = Cadcam.objects.filter(model=i, deleted=False, status="NG")
        waiting = Cadcam.objects.filter(model=i, deleted=False, status="Waiting")
        data1.append(len(ok))
        data2.append(len(ng))
        data3.append(len(waiting))
    labels = ", ".join(labels)
    return render(request, 'base/home.html', {"labels": labels, "data1": data1, "data2": data2, "data3": data3})
