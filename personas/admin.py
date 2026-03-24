from django.contrib import admin
from .models import Persona, StockAlcohol, StockDinero

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'bebida_principal', 'refresco', 'dias', 'ha_pagado', 'cantidad_pagar')
    list_filter = ('dias', 'ha_pagado', 'bebida_principal', 'refresco', 'alcohol')
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


@admin.register(StockAlcohol)
class StockAlcoholAdmin(admin.ModelAdmin):
    list_display = ('bebida', 'cantidad_stock')
    list_editable = ('cantidad_stock',)


@admin.register(StockDinero)
class StockDineroAdmin(admin.ModelAdmin):
    list_display = ('concepto', 'cantidad', 'tipo', 'fecha')
    list_filter = ('tipo',)
    search_fields = ('concepto',)
