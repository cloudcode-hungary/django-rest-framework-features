from django.urls import path

from . import views

urlpatterns = [
    path('api/1/test', views.TestView.as_view(), name='test-view'),
]
