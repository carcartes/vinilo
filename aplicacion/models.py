from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from .opciones import REGIONES_CHILE, CIUDADES_CHILE

class DireccionEnvio(models.Model):
    pedido = models.OneToOneField('Pedido', on_delete=models.CASCADE, related_name='direccion_envio')
    calle = models.CharField(max_length=255)
    region = models.CharField(max_length=100, choices=REGIONES_CHILE)
    ciudad = models.CharField(max_length=100, choices=CIUDADES_CHILE)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"Dirección de envío para el pedido de {self.pedido.user.username}"

class CustomUser(AbstractUser):
    fecha_nacimiento = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Otros campos personalizados si es necesario

    def __str__(self):
        return self.username
    
class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Disco(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    año_publicacion = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to="discos", null=True)
    stock = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En_camino', 'En camino'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    nombre_usuario = models.CharField(max_length=150)  # Campo para almacenar el nombre de usuario
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def save(self, *args, **kwargs):
        # Guardar el nombre de usuario al crear o actualizar el pedido
        if self.user:
            self.nombre_usuario = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido de {self.nombre_usuario} - {self.fecha_pedido}"

        
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    disco = models.ForeignKey(Disco, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    tarjeta_numero = models.CharField(max_length=16)
    tarjeta_caducidad = models.CharField(max_length=5)
    tarjeta_cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Detalle de pedido: {self.disco.titulo} - Cantidad: {self.cantidad}"

class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disco = models.ForeignKey(Disco, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Carrito de {self.usuario.username} - {self.disco.titulo}"

