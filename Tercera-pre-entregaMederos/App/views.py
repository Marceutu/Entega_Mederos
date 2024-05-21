
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render 
from .forms import AnimalForm, PerroForm, GatoForm,UsuarioForm
from .models import Gato, Perro
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



from .models import Animal
from django.http import Http404 


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            contraseña = form.cleaned_data['contraseña']
            user = authenticate(request, username=nombre_usuario, password=contraseña)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Nombre de usuario o contraseña incorrectos.'})
    else:
        form = UsuarioForm()
    return render(request, 'login.html', {'form': form})


@login_required
def protected_view(request):
    user = request.user
    usuario = UsuarioForm.objects.filter(owner=user)
    context = {
        'username': user.username,
    }
    return render(request, 'some_template.html', context)

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def ingresar_perro(request):
    if request.method == 'POST':
        perro_form = PerroForm(request.POST)
        if perro_form.is_valid():
            perro_form.save()
            messages.success(request, "El perro se ha guardado correctamente.")
            return redirect('ingresar_perro')  # Redirige a la misma vista después de guardar
    else:
        perro_form = PerroForm()
    
    return render(request, 'ingresar_perro.html', {'perro_form': perro_form})

@login_required
def ingresar_gato(request):
    if request.method == 'POST':
        gato_form = GatoForm(request.POST)
        if gato_form.is_valid():
            gato_form.save()
            messages.success(request, "El gato se ha guardado correctamente.")
            return redirect('ingresar_gato')  # Redirige a la misma vista después de guardar
    else:
        gato_form = GatoForm()
    
    return render(request, 'ingresar_gato.html', {'gato_form': gato_form})

def home(request):
    return render(request, 'index.html')


def contacto(request):
    return render(request, 'contacto.html')

def informacion(request):
    return render(request, 'informacion.html')

@login_required
def buscar_animal(request):
    if request.method == 'POST':
        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')
        
        if sexo in ['Macho', 'Hembra'] and edad.isdigit():
            animales = Animal.objects.filter(sexo=sexo, edad=edad)
            if animales.exists():
                return render(request, 'core/resultados_busqueda.html', {'animales': animales})
            else:
                messages.info(request, 'No se encontraron animales con los criterios de búsqueda especificados.')
        else:
            messages.error(request, 'Los valores de sexo y edad son inválidos.')
        
        return redirect('buscar')  # Redirige a la página de búsqueda para que los mensajes se muestren
    
    return render(request, 'core/buscar.html')


def mostrar_animal(request):
    # Tu lógica para mostrar los detalles del animal aquí
    return render(request, 'core/mostrar_animal.html', {'animal': None})

def resultados_busqueda(request):
    if request.method == 'POST':
        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')

        # Buscar animales que coincidan con el sexo y la edad proporcionados
        animales = Animal.objects.filter(sexo=sexo, edad=edad)

        # Verificar si se encontraron animales que coincidan con los criterios de búsqueda
        if animales.exists():
            # Eliminar todos los animales encontrados
            animales.delete()
            return JsonResponse({'message': '¡Los animales se han eliminado con éxito!'})
        else:
            return JsonResponse({'error': 'No se encontraron animales con los criterios de búsqueda especificados.'}, status=404)
        
    
def editar_animal(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La modificación se ha procesado con éxito!')
            return redirect('buscar')
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'core/editar_animal.html', {'form': form, 'animal_id': animal_id})




def eliminar_animal(request):
    # Obtener el animal por su ID
    animal = get_object_or_404(Animal)
    
    if request.method == 'POST':
        # Obtener sexo y edad del animal de la solicitud POST
        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')
        
        # Verificar si el sexo y la edad coinciden
        if animal.sexo == sexo and animal.edad == edad:
            animal.delete()
            messages.success(request, '¡El animal se ha eliminado con éxito!')
            return redirect('resultados_busqueda')
        else:
            messages.error(request, 'Los datos de sexo y edad no coinciden.')
    
    return render(request, 'core/eliminar_animal.html', {'animal': animal})

def home_view(request):
    return render(request, 'home.html')