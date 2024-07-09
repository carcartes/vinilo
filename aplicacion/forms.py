from django import forms
from .models import Disco, Pedido, CustomUser, DireccionEnvio, PedidoDetalle
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
import re


class DireccionEnvioForm(forms.ModelForm):

    class Meta:
        model = DireccionEnvio  
        fields = ['calle', 'region', 'ciudad', 'codigo_postal']  
        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),  # Utilizamos Select para campos con opciones
            'ciudad': forms.Select(attrs={'class': 'form-control'}),  # Utilizamos Select para campos con opciones
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_calle(self):
        calle = self.cleaned_data.get('calle', '')
        if len(calle) > 15:
            raise forms.ValidationError("La calle no puede tener más de 15 caracteres.")
        elif len(calle) <= 4:
            raise forms.ValidationError("La calle debe tener más de 4 caracteres.")
        return calle
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data['codigo_postal']
        # Validar longitud exacta
        if len(codigo_postal) != 7:
            raise forms.ValidationError('El código postal debe tener exactamente 7 dígitos.')
        # Validar que sean solo números
        if not codigo_postal.isdigit():
            raise forms.ValidationError('El código postal debe contener solo números.')

        return codigo_postal

class DatosTarjetaForm(forms.Form):
    numero_tarjeta = forms.CharField(label='Número de Tarjeta', max_length=16)

    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data['numero_tarjeta']
        if not numero_tarjeta.isdigit() or len(numero_tarjeta) != 16:
            raise forms.ValidationError('El número de tarjeta debe tener exactamente 16 dígitos y contener solo números.')
        return numero_tarjeta

    caducidad_tarjeta = forms.DateField(
        label='Fecha de Caducidad',
        input_formats=['%m/%Y'],
        widget=forms.DateInput(format='%m/%Y')
    )

    def clean_caducidad_tarjeta(self):
        caducidad_tarjeta = self.cleaned_data['caducidad_tarjeta']
        if caducidad_tarjeta < timezone.now().date():
            raise forms.ValidationError('La fecha de caducidad debe ser mayor a la fecha actual.')
        return caducidad_tarjeta

    cvv_tarjeta = forms.CharField(label='CVV', max_length=3)

    def clean_cvv_tarjeta(self):
        cvv_tarjeta = self.cleaned_data['cvv_tarjeta']
        if not cvv_tarjeta.isdigit() or len(cvv_tarjeta) != 3:
            raise forms.ValidationError('El CVV debe tener exactamente 3 dígitos y contener solo números.')
        return cvv_tarjeta

class DiscoForm(forms.ModelForm):
    class Meta:
        model = Disco
        fields = '__all__'

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 3 or len(titulo) > 25:
            raise forms.ValidationError("El título debe tener entre 3 y 20 caracteres.")
        return titulo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser menor que cero.")
        return precio

    def clean_año_publicacion(self):
        año_publicacion = self.cleaned_data.get('año_publicacion')
        año_actual = timezone.now().year
        if año_publicacion >= año_actual:
            raise forms.ValidationError("El año de publicación debe ser menor al año actual.")
        return año_publicacion

class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 15:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 15 caracteres.")
        return username   

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            if fecha_nacimiento.year < 1900 or fecha_nacimiento > timezone.now().date():
                raise forms.ValidationError("La fecha de nacimiento debe estar entre 1900 y la fecha actual.")
        return fecha_nacimiento

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras.")
        elif len(first_name) < 3 or len(first_name) > 12:
            raise forms.ValidationError("El nombre debe tener entre 3 y 12 caracteres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido debe contener solo letras.")
        elif len(last_name) < 3 or len(last_name) > 12:
            raise forms.ValidationError("El apellido debe tener entre 3 y 12 caracteres.")
        return last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        
        if commit:
            user.save()
        return user

class UpdCustomUserCreationForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    imagen = forms.ImageField(label='Imagen de Perfil', required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'fecha_nacimiento', 'email', 'imagen']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 15:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 15 caracteres.")
        return username   

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras.")
        elif len(first_name) < 3 or len(first_name) > 12:
            raise forms.ValidationError("El nombre debe tener entre 3 y 12 caracteres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido debe contener solo letras.")
        elif len(last_name) < 3 or len(last_name) > 12:
            raise forms.ValidationError("El apellido debe tener entre 3 y 12 caracteres.")
        return last_name

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            if fecha_nacimiento.year < 1900 or fecha_nacimiento > timezone.now().date():
                raise forms.ValidationError("La fecha de nacimiento debe estar entre 1900 y la fecha actual.")
        return fecha_nacimiento

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['user', 'estado' ]