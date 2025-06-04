from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),  # domain root
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Superadmin routes
    # path('superadmin/dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    
    # Admin routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/create-admin/', views.create_admin, name='create_admin'),
    path('admin/problem/add/', views.add_problem, name='add_problem'),
    path('admin/problem/delete/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('admin/update_problems/', views.update_problems, name='update_problems'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # User routes
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('progress/', views.user_progress_view, name='user_progress_view'),
    path('save_note/<int:problem_id>/', views.save_note, name='save_note'),
    path('toggle_progress/<int:problem_id>/', views.toggle_progress, name='toggle_progress'),
    path('statistics/', views.get_user_statistics, name='get_user_statistics'),
]
