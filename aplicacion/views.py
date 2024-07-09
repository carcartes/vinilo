# IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disco, Pedido, CustomUser, Carrito, DireccionEnvio, PedidoDetalle
from .forms import DiscoForm, CustomUserCreationForm, PedidoForm, UpdCustomUserCreationForm, DatosTarjetaForm, DireccionEnvioForm
from django.contrib import messages
from os import remove, path
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import HttpResponseServerError
from django.http import JsonResponse
from datetime import date


def index(request):
    return render(request,'aplicacion/index.html')

def catalogo(request):
    discos = Disco.objects.filter(stock__gt=0)  # Filtrar discos con stock mayor que cero
    
    context = {
        'discos': discos
    }
    return render(request, 'aplicacion/catalogo.html', context)

# LOGIN

def salir(request):
    logout(request)
    messages.success(request, "Se ha cerrado sesion correctamente")
    return redirect(to='index')
    
def registrar(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method =='POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al inicio
            return redirect(to=index)
        data["form"] = formulario

    return render(request, 'registration/registrar.html', data)

# COMPRAS

@login_required
def realizar_pedido(request):
    if request.method == 'POST':
        return process_pedido(request)

    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.disco.precio * item.cantidad for item in carrito)

    context = {
        'carrito': carrito,
        'total': total,
        'datos_tarjeta_form': DatosTarjetaForm(),
    }

    return render(request, 'aplicacion/ver_carrito.html', context)

@login_required
def pagar_tarjeta(request):
    if request.method == 'POST':
        return process_pedido(request)

    context = {
        'datos_tarjeta_form': DatosTarjetaForm(),
    }

    return render(request, 'aplicacion/pagar_tarjeta.html', context)


def direccion_envio(request):
    if request.method == 'POST':
        direccion_form = DireccionEnvioForm(request.POST)
        if direccion_form.is_valid():
            direccion = direccion_form.save(commit=False)
            direccion.pedido = crear_pedido(request.user)
            direccion.save()
            return redirect('pagar_tarjeta')  # Ajusta esta URL según la vista de confirmación de pago
    else:
        direccion_form = DireccionEnvioForm()
    
    return render(request, 'aplicacion/direccion_envio.html', {'direccion_form': direccion_form})

def crear_pedido(usuario):
    carrito = Carrito.objects.filter(usuario=usuario)
    pedido = Pedido.objects.create(user=usuario)

    try:
        with transaction.atomic():
            for item in carrito:
                # Crear el detalle de pedido
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    disco=item.disco,
                    cantidad=item.cantidad,
                )
                
                # Actualizar el stock del disco
                disco = item.disco
                disco.stock -= item.cantidad
                disco.save()

            # Una vez procesados todos los detalles del pedido, eliminar el carrito
            carrito.delete()

    except Exception as e:
        raise e

    return pedido

@login_required
def process_pedido(request):
    datos_tarjeta_form = DatosTarjetaForm(request.POST)
    if not datos_tarjeta_form.is_valid():
        # Manejar error en formulario de tarjeta inválido
        messages.error(request, 'Error en los datos de la tarjeta. Por favor, revisa nuevamente.')
        return redirect('pagar_tarjeta')

    try:
        with transaction.atomic():
            # Guardar pedido con la fecha y hora registradas automáticamente
            for item in Carrito.objects.filter(usuario=request.user):
                Pedido.objects.create(
                    user=request.user,
                    disco=item.disco,
                    cantidad=item.cantidad,
                    tarjeta_numero=datos_tarjeta_form.cleaned_data['numero_tarjeta'],
                    tarjeta_caducidad=datos_tarjeta_form.cleaned_data['caducidad_tarjeta'],
                    tarjeta_cvv=datos_tarjeta_form.cleaned_data['cvv_tarjeta']
                )
                item.delete()

        messages.success(request, '¡Pedido realizado correctamente!')
        return redirect('index')  # Redirigir al inicio después de completar el pedido

    except Exception as e:
        print(f"Error al realizar pedido: {e}")
        return HttpResponseServerError("Error al procesar el pedido. Inténtalo de nuevo más tarde.")

# CARRITO

@login_required
def eliminar_del_carrito(request, id):
    item = get_object_or_404(Carrito, id=id)
    
    if request.method == "POST":
        item.delete()
        messages.success(request, "Ítem eliminado del carrito correctamente.")
    
    return redirect('ver_carrito')

@login_required
def agregar_al_carrito(request, id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir al login si el usuario no está autenticado
    
    disco = get_object_or_404(Disco, id=id)
    
    # Verificar si la cantidad que se quiere agregar supera el stock disponible
    if disco.stock <= 0:
        messages.error(request, 'Este disco está fuera de stock.')
        return redirect('ver_catalogo')  # Redirigir a alguna página o vista que muestre el catálogo
    
    carrito_item, created = Carrito.objects.get_or_create(usuario=request.user, disco=disco)
    
    if not created:
        # Si el ítem ya existe en el carrito, verificar si se puede incrementar la cantidad
        if carrito_item.cantidad >= disco.stock:
            messages.warning(request, 'No se puede agregar más unidades, ha alcanzado el límite de stock.')
        else:
            carrito_item.cantidad += 1
            carrito_item.save()
    else:
        # Si es un nuevo ítem en el carrito, verificar si hay stock disponible
        if disco.stock <= 0:
            messages.error(request, 'Este disco está fuera de stock.')
        else:
            carrito_item.cantidad = 1
            carrito_item.save()
    
    return redirect('ver_carrito')  # Redirigir a la vista del carrito después de agregar al carrito

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.disco.precio * item.cantidad for item in carrito)
    context = {
        'carrito': carrito,
        'total': total,
    }
    return render(request, 'aplicacion/ver_carrito.html', context)

@login_required
def actualizar_cantidad(request, id):
    carrito_item = get_object_or_404(Carrito, id=id)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Verificar si la cantidad ingresada es válida
        if cantidad > 0:
            # Verificar si la cantidad no supera el stock disponible del disco
            if cantidad <= carrito_item.disco.stock:
                carrito_item.cantidad = cantidad
                carrito_item.save()
            else:
                messages.warning(request, f"No puedes agregar más de {carrito_item.disco.stock} unidades.")
        else:
            messages.error(request, "La cantidad debe ser mayor que cero.")
    
    return redirect('ver_carrito')



#ADMIN

@permission_required('aplicacion.view_disco')
def listar_discos(request):
    discos = Disco.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(discos, 5)
        discos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': discos,
        'paginator': paginator
    }
    return render(request,'aplicacion/administrador/listar.html', data)

@permission_required('aplicacion.add_disco')
def agregar_disco(request):
    data = {
        'form': DiscoForm()
    }
    
    if request.method == 'POST':
        formulario = DiscoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"producto registrado")
            return redirect(to="listar_discos")
        else:
            data["form"] = formulario
    return render(request, 'aplicacion/administrador/agregar.html', data)

@permission_required('aplicacion.change_disco')
def modificar_disco(request, id):
    
    disco = get_object_or_404(Disco, id=id)

    data = {
        'form' : DiscoForm(instance=disco)
    }
    
    if request.method == 'POST':
        formulario = DiscoForm(data=request.POST, instance=disco, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="listar_discos")
        data["form"] = formulario

    return render(request, 'aplicacion/administrador/modificar.html', data)

@permission_required('aplicacion.delete_disco')
def eliminar_disco(request, id):
    producto = get_object_or_404(Disco, id=id)
    producto.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_discos")


@permission_required('aplicacion.add_disco')
def personas(request):
    personas = CustomUser.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(personas, 5)
        personas = paginator.page(page)
    except:
        raise Http404
    
    datos = {
        'entity': personas,
        'paginator': paginator
    }

    return render(request, 'aplicacion/administrador/personas.html', datos)

@permission_required('aplicacion.add_disco')
def crearpersona(request):
    
    formulario=CustomUserCreationForm()

    if request.method=="POST":
        formulario=CustomUserCreationForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            #from django.contrib import messages
            messages.set_level(request,messages.SUCCESS)
            messages.success(request, "Persona creada con exito!!!")
            return redirect(to="personas")
        
    datos={
        "formulario":formulario
    }

    return render(request,'aplicacion/administrador/crearpersona.html', datos)

@permission_required('aplicacion.add_disco')
def modificarpersona(request, id):
    user = get_object_or_404(CustomUser, id=id)
    form = UpdCustomUserCreationForm(instance=user)
    
    if request.method == "POST":
        form = UpdCustomUserCreationForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="personas")  
    
    datos = {
        'user': user,
        'form': form
    }
    return render(request, 'aplicacion/administrador/modificarpersona.html', datos)

@permission_required('aplicacion.add_disco')
def eliminarpersona(request, id):
    user = get_object_or_404(CustomUser, id=id)
    
    if request.method == "POST":
        if user.imagen:
            # Eliminar la imagen asociada si existe
            try:
                remove(path.join(str(settings.MEDIA_ROOT).replace('/media', '') + str(user.imagen.url).replace('/', '\\')))
            except FileNotFoundError:
                pass  # Manejar caso donde la imagen ya ha sido eliminada externamente
        
        user.delete()
        
        messages.set_level(request, messages.WARNING)
        messages.warning(request, "Persona Eliminada")
        return redirect(to="personas")
    
    datos = {
        'user': user,
    }
    return render(request, 'aplicacion/administrador/eliminarpersona.html', datos)

@permission_required('aplicacion.add_disco')
def pedidos(request):
    pedidos=Pedido.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(pedidos, 5)
        pedidos =  paginator.page(page)
    except:
        raise Http404
    
    datos= {
        'entity':pedidos,
        'paginator': paginator
    }

    return render(request,'aplicacion/administrador/pedidos.html', datos)

@permission_required('aplicacion.add_disco')
def detalles_pedido(request, pedido_id):
    # Obtener el pedido por su ID, si no existe devuelve un error 404
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Calcular el total del pedido
    total_pedido = sum(detalle.disco.precio * detalle.cantidad for detalle in pedido.detalles.all())
    
    # Datos a pasar a la plantilla
    datos = {
        'pedido': pedido,
        'total_pedido': total_pedido,  # Incluimos el total del pedido en los datos
    }
    
    return render(request, 'aplicacion/administrador/detalles_pedido.html', datos)

@permission_required('aplicacion.add_disco')
def modificarpedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    direccion_envio = pedido.direccion_envio

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, instance=pedido)
        direccion_form = DireccionEnvioForm(request.POST, instance=direccion_envio)

        if pedido_form.is_valid() and direccion_form.is_valid():
            pedido_form.save()
            direccion_form.save()
            messages.success(request, "Pedido y dirección de envío modificados correctamente")
            return redirect('pedidos')

    else:
        pedido_form = PedidoForm(instance=pedido)
        direccion_form = DireccionEnvioForm(instance=direccion_envio)

    context = {
        'pedido_form': pedido_form,
        'direccion_form': direccion_form,
    }

    return render(request, 'aplicacion/administrador/modificarpedido.html', context)
@permission_required('aplicacion.add_disco')
def eliminarpedido(request,id):
    pedido=get_object_or_404(Pedido, id=id)
    
    if request.method=="POST":
        pedido.delete()
        
        messages.set_level(request,messages.WARNING)
        messages.warning(request,"Pedido Eliminado")
        return redirect(to="pedidos")
    
    datos={
        'pedido':pedido,
    
    }
    return render(request,'aplicacion/administrador/eliminarpedido.html',datos)

@permission_required('aplicacion.add_disco')
def crearpedido(request):
    
    formulario=PedidoForm()

    if request.method=="POST":
        formulario=PedidoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            #from django.contrib import messages
            messages.set_level(request,messages.SUCCESS)
            messages.success(request, "Pedido creado con exito!!!")
            return redirect(to="pedidos")
        
    datos={
        "formulario":formulario
    }

    return render(request,'aplicacion/administrador/crearpedido.html', datos)

# PERFIL

@login_required
def perfil_usuario(request):
    usuario = request.user
    context = {
        'usuario': usuario
    }
    return render(request, 'aplicacion/perfil_usuario.html', context)

@login_required
def mispedidos(request):
    pedidos = Pedido.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(pedidos,5)
        pedidos = paginator.page(page)
    except:
        raise Http404
    context = {
        'entity': pedidos,
        'paginator': paginator
    }
    return render(request,'aplicacion/mispedidos.html',context)

@login_required
def detalles_pedido_usuario(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    
    # Calcular el total del pedido
    total_pedido = sum(detalle.disco.precio * detalle.cantidad for detalle in pedido.detalles.all())
    
    context = {
        'pedido': pedido,
        'total_pedido': total_pedido,
    }
    return render(request, 'aplicacion/detalles_pedido_usuario.html', context)


@login_required
def modificarperfil(request, id):
    user = get_object_or_404(CustomUser, id=id)
    form = UpdCustomUserCreationForm(instance=user)
    
    if request.method == "POST":
        form = UpdCustomUserCreationForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil modificado correctamente")
            return redirect('perfil_usuario')  # Redirigir al perfil del usuario después de guardar los cambios
    
    datos = {
        'user': user,
        'form': form
    }
    return render(request, 'aplicacion/modificarperfil.html', datos)
