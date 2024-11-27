from django.shortcuts import render, redirect
from django.contrib.auth import login
from reservas.models import Reserva
from .forms import ClienteForm, ReservaForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from reservas.models import Cliente
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

@login_required
def lista_reservas(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Acesso negado.")
    
    reservas = Reserva.objects.all()
    return render(request, 'lista_reservas.html', {'reservas': reservas})

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Cliente.objects.filter(email=email).exists():
                form.add_error('email', 'Este email já está registrado.')
            else:
                senha = form.cleaned_data['senha']

                cliente = form.save(commit=False)
                cliente.senha = senha 
                cliente.save()

                return redirect('reservas:sucesso')

    else:
        form = ClienteForm()

    return render(request, 'cadastrar.html', {'form': form})

def login_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            cliente = get_user_model().objects.get(email=email)
            if cliente.check_password(password):
                login(request, cliente)
                return redirect('reserva')
            else:
                return HttpResponseForbidden("Senha incorreta.")
        except get_user_model().DoesNotExist:
            return HttpResponseForbidden("Email não encontrado.")

    return render(request, 'login.html')

@login_required
def reservar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user.cliente
            reserva.save()
            return redirect('reservas:sucesso')
    else:
        form = ReservaForm()

    return render(request, 'reserva.html', {'form': form})

from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'auth_user': request.user})
    return render(request, 'index.html')

def sucesso(request):
    return render(request, 'sucesso.html')