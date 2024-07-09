from django.contrib import admin
from .models import Artista, Genero, Disco, Pedido, CustomUser, Carrito, DireccionEnvio, PedidoDetalle

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'imagen']
    list_filter = ['fecha_nacimiento']
    search_fields = ['username', 'email']

class DiscoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "artista", "genero", "año_publicacion", "precio", "stock"]
    list_filter = ["artista", "genero"]
    search_fields = ["titulo", "artista__nombre", "genero__nombre"]

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['user', 'fecha_pedido']
    list_filter = ['user']
    search_fields = ['user__username', 'disco__titulo']

class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'disco', 'cantidad']
    list_filter = ['usuario', 'disco']
    search_fields = ['usuario__username', 'disco__titulo']

class PedidoDetalleAdmin(admin.ModelAdmin):
    list_display = ["pedido", "disco", "cantidad"]

admin.site.register(Artista)
admin.site.register(Disco, DiscoAdmin)
admin.site.register(Genero)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(PedidoDetalle,PedidoDetalleAdmin)
