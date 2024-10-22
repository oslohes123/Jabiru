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
    path('dashboard/assign_child/', views.assign_child, name='assign_child'),
    path('make_request_for_child/', views.make_request_for_child, name='make_request_for_child'),
    path('fill_make_request_for_child/', views.fill_make_request_for_child, name='fill_make_request_for_child'),
    path('delete_administrator/', views.delete_administrator, name='delete_administrator'),
    path('edit_administrator/', views.edit_administrator, name='edit_administrator'),
    path('fill_edit_administrator/', views.fill_edit_administrator, name='fill_edit_administrator'),
    path('transactions_and_invoice/', views.return_transactions_and_invoice, name="return_transaction_and_invoice_for_approved"),
    path('make_payment/', views.make_payment_approved_lesson, name="make_payment_approved_lesson"),
    path('edit_unapproved_lessons/', views.edit_unapproved_lessons, name='edit_unapproved_lessons'),
    path('fill_edit_unapproved_lessons/', views.fill_edit_unapproved_lessons, name='fill_edit_unapproved_lessons'),
    path('delete_request/', views.delete_request, name='delete_request'),
    path('make_super_administrator/', views.make_super_administrator, name='make_super_administrator'),
    path('dashboard/search_student_lessons/', views.get_requests, name='get_requests'),
    path('fill_in_approve_request/', views.fill_in_approve_request, name='fill_in_approve_request'),
    path('approve_request/', views.approve_request, name='approve_request'),
    path('edit_approved_lessons/', views.edit_approved_lessons, name='edit_approved_lessons'),
    path('fill_edit_approved_lessons/', views.fill_edit_approved_lessons, name='fill_edit_approved_lessons'),
    path('delete_approved_lesson/', views.delete_approved_lesson, name='delete_approved_lesson'),
    path('view_transactions/',views.admin_view_transactions_specific_student,name="view_transactions_specific_student"),
    path('view_transactions_all/',views.admin_view_transactions_of_all,name="view_transactions_all_students"),
    path('approve_request/', views.approve_request, name='approve_request')

]
