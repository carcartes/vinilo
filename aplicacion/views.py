from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'aplicacion/index.html')

def catalogo(request):
    return render(request,'aplicacion/catalogo.html')

#LOGIN

def iniciar(request):
    return render(request,'aplicacion/login/iniciar.html')

def registro(request):
    return render(request,'aplicacion/login/registro.html')

def recuperar(request):
    return render(request,'aplicacion/login/recuperar.html')

def nuevacontra(request):
    return render(request,'aplicacion/login/nuevacontra.html')

def verificar(request):
    return render(request,'aplicacion/login/verificar.html')

#USUARIO INICIADO

def indexiniciado(request):
    return render(request, 'aplicacion/usuario/indexiniciado.html')

def catalogoiniciado(request):
    return render(request, 'aplicacion/usuario/catalogoiniciado.html')

def verpedidos(request):
    return render(request, 'aplicacion/usuario/verpedidos.html')

def checkout(request):
    return render(request, 'aplicacion/usuario/checkout.html')
def pagar(request):
    return render(request, 'aplicacion/usuario/pagar.html')
def comprado(request):
    return render(request, 'aplicacion/usuario/comprado.html')

#ADMIN

def admin(request):
    return render(request, 'aplicacion/administrador/admin.html')

def inventario(request):
    return render(request, 'aplicacion/administrador/inventario.html')

def pedidos(request):
    return render(request, 'aplicacion/administrador/pedidos.html')

def usuarios(request):
    return render(request, 'aplicacion/administrador/usuarios.html')

