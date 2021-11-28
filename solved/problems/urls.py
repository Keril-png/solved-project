from django.urls import path

from . import views

# app_name = 'problems'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('problems/create/', views.new_problem, name = 'new_problem'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('problems/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('problems/<int:problem_id>/edit/', views.edit_problem, name = 'edit_problem'),
    path('problems/<int:problem_id>/delete/', views.delete_problem, name = 'delete_problem'),
    path('problems/<int:problem_id>/download_file/', views.download_file, name = 'download_file')
] 