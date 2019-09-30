from django.urls import path

from . import views

urlpatterns = [
    path('api/1/test/', views.TestListView.as_view(), name='test-list-view'),
    path('api/1/test/<int:pk>/', views.TestRetrieveDestroyView.as_view(), name='test-instance-view'),
]
