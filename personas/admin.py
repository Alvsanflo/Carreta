from django.contrib import admin
from .models import Persona

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'bebida_principal', 'dias', 'ha_pagado', 'cantidad_pagar')
    list_filter = ('dias', 'ha_pagado', 'bebida_principal', 'alcohol')
    search_fields = ('nombre', 'apellidos')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellidos')
        }),
        ('Bebidas', {
            'fields': ('bebida_principal', 'refresco', 'alcohol')
        }),
        ('Asistencia y Pago', {
            'fields': ('dias', 'cantidad_pagar', 'ha_pagado')
        }),
    )
