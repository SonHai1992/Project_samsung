from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# def login(request):
#     return render(request, 'login/login.html')


def my_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        next_page = request.GET.get('next')
        if user is not None:
            login(request, user)
            if next_page:
                return redirect(next_page)

            return redirect('home')
        else:
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')


def my_logout(request):
    logout(request)
    return redirect('login')
