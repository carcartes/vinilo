

from django.urls import path, include
from .views import index, catalogo, iniciar, registro, recuperar, nuevacontra, verificar, catalogoiniciado, indexiniciado, verpedidos, checkout, pagar, comprado, admin, inventario, pedidos, usuarios

urlpatterns = [
    path('',index,name='index'),
    path('catalogo/',catalogo, name='catalogo'),
    path('iniciar/',iniciar, name='iniciar'),
    #LOGIN
    path('login/registro/',registro, name='registro'),
    path('login/recuperar/',recuperar, name='recuperar'),
    path('login/nuevacontra/',nuevacontra, name='nuevacontra'),
    path('login/verificar/',verificar, name='verificar'),
    #USUARIO INICIADO
    path('usuario/indexiniciado/',indexiniciado, name='indexiniciado'),
    path('usuario/catalogoiniciado/',catalogoiniciado, name='catalogoiniciado'),
    path('usuario/verpedidos/',verpedidos, name='verpedidos'),
    path('usuario/checkout/',checkout, name='checkout'),
    path('usuario/pagar/',pagar, name='pagar'),
    path('usuario/comprado/',comprado, name='comprado'),
    #ADMIN
    path('administrador/admin/',admin, name='admin'),
    path('administrador/inventario/',inventario, name='inventario'),
    path('administrador/pedidos/',pedidos, name='pedidos'),
    path('administrador/usuarios/',usuarios, name='usuarios'),

    
]