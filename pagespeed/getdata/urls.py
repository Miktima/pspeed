from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results.html', views.results, name='results'),
    path('saved_results/<int:portal_id>/', views.saved_results, name='saved_results'),
    path('home.html', views.save_data, name='save_data'),
]