from django.contrib import admin
from .models import Mesa, Reserva, Funcionario

admin.site.register(Mesa)
admin.site.register(Funcionario)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('mesa', 'cliente_nome', 'data', 'hora', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__username', 'cliente__email')  

    def cliente_nome(self, obj):
        return obj.cliente.username 
    cliente_nome.admin_order_field = 'cliente'  
    cliente_nome.short_description = 'Cliente'