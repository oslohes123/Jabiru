from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lessons.forms import LogInForm



# Create your views here.


def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        nextItem = request.POST.get('nextItem') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = nextItem or 'feed'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        nextItem = request.GET.get('nextItem') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'nextItem': nextItem})


def home(request):
    return render(request, 'home.html')

