from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('result/<artist_name>/', views.results, name='results'),
]
