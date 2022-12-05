from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name="login_user"),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out/', views.log_out, name='log_out'),
    path('make_request/', views.make_request, name='make_request'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sign_up_administrator/', views.sign_up_administrator, name='sign_up_administrator'),
    path('view_all_administrators/', views.view_all_administrators, name='view_all_administrators'),
    path('delete_administrator/(?P<email>\d+)', views.delete_administrator, name='delete_administrator'),
    path('edit_administrator/(?P<email>\d+)', views.edit_administrator, name='edit_administrator'),
    path('edit_unapproved_lessons/<str:lesson_key>/', views.edit_unapproved_lessons, name='edit_unapproved_lessons'),
    # change the key in the str<>, to the actually key when made
    path('delete_lesson/<str:lesson_key>/', views.delete_request, name='delete_request'),
    path('make_super_administrator/', views.make_super_administrator, name='make_super_administrator'),
    path('dashboard/search_student_lessons', views.get_requests, name='get_requests'),
    path('fill_in_approve_request/', views.fill_in_approve_request, name='fill_in_approve_request'),
    path('approve_request/', views.approve_request, name='approve_request')
]
