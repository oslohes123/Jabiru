from django.shortcuts import render
from .forms import SignUpForm
# Create your views here.
def sign_up(request):
    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})