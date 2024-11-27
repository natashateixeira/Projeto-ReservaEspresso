from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField()
    disponibilidade = models.BooleanField(default=True)
    localizacao = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Mesa {self.numero} - Disponível: {self.disponibilidade} - Capacidade: {self.capacidade}"

    def verificar_disponibilidade(self, data, hora):
        reservas_conflitantes = Reserva.objects.filter(mesa=self, data=data, hora=hora, status="CONFIRMADA")
        return not reservas_conflitantes.exists()

class Reserva(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada")
    ]
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)
    data = models.DateField()
    hora = models.TimeField()
    numero_pessoas = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")

    def clean(self):
        
        if self.numero_pessoas > self.mesa.capacidade:
            raise ValidationError(f'O número de pessoas não pode ultrapassar a capacidade da mesa {self.mesa.numero}.')
        if not self.mesa.verificar_disponibilidade(self.data, self.hora):
            raise ValidationError(f'A Mesa {self.mesa.numero} já está reservada para esse horário.')

    def __str__(self):
        return f'Reserva {self.id} - {self.cliente.nome} para Mesa {self.mesa.numero} em {self.data} às {self.hora}'


class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente', null=True, blank=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=16, null=False, default='senha_temporal')

    def __str__(self):
        return self.nome
class Funcionario(models.Model):
    CARGO_CHOICES = [
        ('ATENDENTE', 'Atendente - Garçom'),
        ('CAIXA', 'Caixa'),
        ('GERENTE', 'Gerente'),
    ]

    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50, choices=CARGO_CHOICES, default='Desconhecido')
    telefone = models.CharField(max_length=20, default='000000000')

    def __str__(self):
        return f"{self.nome} - {self.cargo}"
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set', 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set', 
        blank=True,
    )

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']