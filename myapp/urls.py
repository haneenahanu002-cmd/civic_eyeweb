"""Civic_Eye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login/',views.login_get),
    path('login_post/',views.login_post),
    path('a_home/',views.a_home),
    path('add_department/',views.add_department),
    path('add_department_post/',views.add_department_post),
    path('view_department/',views.view_department),
    path('edit_department/<id>',views.edit_department),
    path('edit_department_post/',views.edit_department_post),
    path('view_registered/',views.view_registered),
    path('change_password/',views.change_password),
    path('change_password_post/',views.change_password_post),
    path('view_appreview/', views.view_appreview),
    path('view_complaint/',views.view_complaint),
    path('viewcomplaint_more/<id>',views.viewcomplaint_more),
    path('dept_view_profile/',views.dept_view_profile),
    path('dept_change_password/',views.dept_change_password),
    path('viewfiltered_complaint/',views.viewfiltered_complaint),
    path('take_action/<id>',views.take_action),
    path('create_action/<id>',views.create_action),
    path('dept_home/', views.dept_home),
    path('delete_department/<id>',views.delete_department),
    path('create_action_post/',views.create_action_post),
    path('admin_view_dashboard/',views.admin_view_dashboard),
    path('logout_get/',views.logout_get),
    path('check/',views.check),
    path('change_status/',views.change_status),







#==========User=============#=============
    path('user_signup/',views.user_signup),
    path('user_login/',views.user_login),
    path('user_viewprofile/', views.user_viewprofile),
    path('user_editprofile/', views.user_editprofile),
    path('user_sendcomplaint/', views.user_sendcomplaint),
    path('user_viewcomplaint/', views.user_viewcomplaint),
    path('user_changepassword/', views.user_changepassword),
    path('user_sendappreview/', views.user_sendappreview),
    path('user_viewappreview/', views.user_viewappreview),
    path('android_forget_password_post/', views.android_forget_password_post),
    path('forget_password/', views.forget_password),

]
