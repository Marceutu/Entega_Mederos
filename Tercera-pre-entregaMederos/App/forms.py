from django import forms
from .models import Animal, Usuario
from .models import Perro, Gato

class PerroForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = '__all__'

class GatoForm(forms.ModelForm):
    class Meta:
        model = Gato
        fields = '__all__'

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['sexo', 'edad', 'descripcion', 'estado_salud']        

class UsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario', max_length=100)
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput())