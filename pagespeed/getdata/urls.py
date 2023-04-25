from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results.html', views.results, name='results'),
    path('saved_results/<int:portal_id>/', views.saved_results, name='saved_results'),
    path('save_data.html', views.save_data, name='save_data'),
    path('sputnik_results/', views.sputnik_results, name='sputnik_results'),
    path('collect_results/', views.collect_results, name='collect_results'),
]