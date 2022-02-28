from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    # 用name取一个别名
    path('project/', views.project, name="project"),
    path('test_case/', views.test_case, name="test_case"),
]