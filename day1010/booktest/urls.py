from django.urls import path, include
from booktest import views

urlpatterns = [
    path('show_args1/<int:a>/<int:b>',views.show_args,name='show_args'),
    path('show_kwargs1/<int:c>/<int:d>',views.show_kwargs,name='show_kwargs'),
]
