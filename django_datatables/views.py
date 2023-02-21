from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Programador

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')

@login_required
def programadores(request):
    ProgramadoresListados = Programador.objects.filter(user=request.user)
    return render(request, 'programadores.html', {"programador": ProgramadoresListados})

@login_required
def agregar_programador(request):
    
    if request.method == 'GET':
        return render(request, 'agregar_programador.html')
    else:
        Nombre = request.POST['Nombre']
        Pais = request.POST['Pais']
        Fecha_nam = request.POST['Fecha_nam']
        Puntuacion = request.POST['Puntuacion']
        email = request.POST['email']
        usuario = request.user

        programador = Programador.objects.create(
            Nombre=Nombre, Pais=Pais, Fecha_nam=Fecha_nam, Puntuacion=Puntuacion, email=email, user=usuario)
        return redirect('programadores') 

@login_required
def edicionProgramador(request, id):
    programador = Programador.objects.get(id=id)
    return render(request, 'editar_programador.html', {"programador": programador})

@login_required
def editar_programador(request):
    Nombre = request.POST['Nombre']
    Pais = request.POST['Pais']
    Fecha_nam = request.POST['Fecha_nam']
    Puntuacion = request.POST['Puntuacion']
    email = request.POST['email']
    usuario = request.user
    
    programador = Programador.objects.get(Nombre=Nombre)
    programador.Nombre = Nombre
    programador.Pais = Pais
    programador.Fecha_nam = Fecha_nam
    programador.Puntuacion = Puntuacion
    programador.email = email
    programador.user = usuario
    programador.save()

    return redirect('programadores')

@login_required
def eliminarProgramador(request, id):
    programador = Programador.objects.get(id=id)
    programador.delete()

    return redirect('programadores')

@login_required
def signout(request):
    logout(request)
    return redirect('home')