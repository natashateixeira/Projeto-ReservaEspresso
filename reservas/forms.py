from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):

    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    senha_confirmada = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Senha")
    nome = forms.CharField(label="Nome Completo", max_length=100)
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email', 'senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha_confirmada = cleaned_data.get('senha_confirmada')

        if senha != senha_confirmada:
            raise forms.ValidationError("As senhas não coincidem.")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class ReservaForm(forms.Form):
    data_reserva = forms.DateField(widget=forms.SelectDateWidget)
    hora_reserva = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    numero_pessoas = forms.IntegerField(min_value=1)
    mesa = forms.IntegerField(min_value=1)  # Supondo que cada reserva tenha um número de mesa
    cliente_email = forms.EmailField(max_length=100, required=False)  # Email será preenchido automaticamente
    cliente_nome = forms.CharField(max_length=100, required=False)  # Nome será preenchido automaticamente

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o usuário logado da view
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            # Pega o cliente logado associado ao usuário
            cliente = Cliente.objects.get(user=user)

            # Preenche os campos com os dados do cliente logado
            self.fields['cliente_nome'].initial = cliente.nome
            self.fields['cliente_email'].initial = cliente.email

    def clean_cliente_email(self):
        # Como o email já vem preenchido e o cliente não deve alterá-lo, podemos simplesmente retornar o valor
        return self.cleaned_data.get('cliente_email')

    def clean_cliente_nome(self):
        # Como o nome já vem preenchido e o cliente não deve alterá-lo, podemos simplesmente retornar o valor
        return self.cleaned_data.get('cliente_nome')