"""
URL configuration for day1010 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from booktest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index1/', views.index, name='index'),
    path('index2/', views.index2),
    path('books/', views.show_books),
    path('books/<int:bid>', views.detail),
    path('create/', views.create),
    path('delete<int:bid>', views.delete),
    path('aggregate/',views.use_aggregate),
    path('areas/', views.areas),
    path('login/', views.login),
    path('login_check/', views.login_check),
    path('test_ajax/', views.test_ajax),
    path('ajax_handle/', views.ajax_handle),
    path('login_ajax/', views.login_ajax),
    path('login_ajax_check/', views.login_ajax_check),
    path('set_cookie/', views.set_cookie),
    path('get_cookie/', views.get_cookie),
    path('set_session/', views.set_session),
    path('get_session/', views.get_session),
    # path('clear_session/', views.clear_session),
    path('test_var/', views.test_var),
    path('test_filters/', views.test_filters),
    path('test_template_inhert/', views.test_template_inhert),
    path('html_escape/', views.html_escape),
    path('change_pwd/', views.change_pwd),
    path('change_pwd_action/', views.change_pwd_action),
    path('verify_code/', views.verify_code),

    path('url_reverse/', views.url_reverse),
    path('test_redirect/', views.test_redirect),
    path('',include(('booktest.urls','booktest'),namespace = 'booktest')),  # 将那个文件的内容合并过来
    
    path('static_test/', views.static_test),
    path('pic_show/', views.pic_show),
    path('show_upload/', views.show_upload),
    path('upload_handle/', views.upload_handle),
    path('show_area/', views.show_area),
    path('show_area/<int:pindex>', views.show_area),

    path('areas/', views.areas),
    path('prov/',views.prov),
    path('city/<int:pid>',views.city),
    path('dis/<int:pid>',views.city),

    path('tinymce/',include('tinymce.urls')),
    path('show/', views.show),

    path('editor/', views.editor),
]
