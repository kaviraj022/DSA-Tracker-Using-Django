from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),  # domain root
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),

]

# for updation of problems
urlpatterns += [
    path('admin/problem/add/', views.add_problem, name='add_problem'),
    path('admin/problem/edit/<int:problem_id>/', views.edit_problem, name='edit_problem'),
    path('admin/problem/delete/<int:problem_id>/', views.delete_problem, name='delete_problem'),
]
