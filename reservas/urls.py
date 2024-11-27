from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.index, name='index'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('registrar/', views.registrar_cliente, name='registrar'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', LogoutView.as_view(next_page='reservas:index'), name='logout'),
    path('reserva/', views.reservar, name='reserva'),
    path('sucesso/', views.sucesso, name='sucesso'),
]