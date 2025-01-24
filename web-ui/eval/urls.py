from django.urls import path

from . import views

urlpatterns = [    
    path("index", views.index, name="index"),
    path("async-operation/", views.async_operation, name="async_operation"),
    path("analyse-code/", views.analyse_code, name="analyse_code"),
    path('save-all/', views.save_all, name='save_all'),
    path('reset-all/', views.reset_all, name='reset_all'),
    path('log/', views.log_message, name='log_message'),
    path('upload-data/', views.upload_data, name='upload_data'),
    
]