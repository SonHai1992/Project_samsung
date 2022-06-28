from django.shortcuts import render

# Create your views here.

def view_page(request):
    return render(request, 'CAM/cam-results.html')