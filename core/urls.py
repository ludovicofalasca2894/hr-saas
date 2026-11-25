from django.contrib import admin
from django.urls import path
from personale import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('gestione-ferie/', views.gestione_ferie, name='gestione_ferie'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('aggiungi-dipendente/', views.aggiungi_dipendente, name='aggiungi_dipendente'),
    path('elimina-dipendente/<int:dipendente_id>/', views.elimina_dipendente, name='elimina_dipendente'),
]

