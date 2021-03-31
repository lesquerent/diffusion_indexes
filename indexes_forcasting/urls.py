from django.urls import path

from . import views  # importe depuis la racine ('indexes_forcasting') le fichier views

urlpatterns = [
    path('home', views.home, name='home'),  # creer la views home
    path('line_chart/', views.line_chart, name='line_chart'),
    path('line_chart_pred_cac', views.line_chart2, name='line_chart2'),
    path('', views.home1, name='home1'),
]
