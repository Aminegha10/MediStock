
from django.urls import path
from . import views

urlpatterns = [
    
    path('stock', views.stock, name = 'stock'),
    path('addstock', views.addstock, name = 'addmed'),
    path('editstock', views.editstock, name = 'edit'),
    path('update/<str:id>', views.updatestock, name = 'update'),
    path('delete/<str:id>', views.delete, name = 'delete'),
    path('date_exp/',views.filtre_date, name='date_exp'),
    path('qte_min/', views.filtre_qte, name='qte_min'),
    path('tri_par_categorie/',views.order_by_categorie, name='tri_par_categorie'),
    path('tri_par_designation/', views.order_by_designation, name='tri_par_designation'),
    path('notifications/ajax/', views.notifications_ajax, name='notifications_ajax'),



    
]