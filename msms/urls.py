from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_user,name = "login_user"),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('make_request/', views.make_request, name = 'make_request'),
    path('', views.home, name='home'),
]

