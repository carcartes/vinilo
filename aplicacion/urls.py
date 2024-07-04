
from django.urls import path, include
from .views import index, catalogo, agregar_disco, listar_discos, modificar_disco, eliminar_disco,salir, registrar, personas, crearpersona, modificarpersona, eliminarpersona,pedidos, modificarpedido, eliminarpedido, crearpedido, agregar_al_carrito, ver_carrito, realizar_pedido, eliminar_del_carrito, mispedidos, perfil_usuario, modificarperfil,actualizar_cantidad,pagar_tarjeta, direccion_envio
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name='index'),
    path('catalogo/',catalogo, name='catalogo'),
    path('agregar-disco/',agregar_disco, name='agregar_disco'),
    path('listar-discos/',listar_discos, name='listar_discos'),
    path('modificar-disco/<id>/',modificar_disco, name='modificar_disco'),
    path('eliminar-disco/<id>/', eliminar_disco, name="eliminar_disco"),
    path('salir/',salir,name='salir'),
    path('registrar/', registrar, name='registrar'),
    path('personas/', personas, name='personas'),
    path('crearpersona/',crearpersona,name='crearpersona'),
    path('modificarpersona/<id>',modificarpersona, name='modificarpersona'),
    path('eliminarpersona/<id>',eliminarpersona,name='eliminarpersona'),
    path('pedidos',pedidos,name='pedidos'),
    path('modificarpedido/<id>',modificarpedido,name='modificarpedido'),
    path('eliminarpedido/<id>',eliminarpedido,name='eliminarpedido'),
    path('crearpedido/',crearpedido,name='crearpedido'),
    path('agregar-al-carrito/<int:id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', ver_carrito, name='ver_carrito'),
    path('realizar-pedido/', realizar_pedido, name='realizar_pedido'),
    path('eliminar-del-carrito/<int:id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('mispedidos/', mispedidos, name='mispedidos'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('modificarperfil/<int:id>/', modificarperfil, name='modificarperfil'),
    path('actualizar-cantidad/<int:id>/', actualizar_cantidad, name='actualizar_cantidad'),
    path('pagar-tarjeta/', pagar_tarjeta, name='pagar_tarjeta'),
    path('direccion_envio', direccion_envio, name='direccion_envio'),


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)