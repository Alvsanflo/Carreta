from django.db import models

DIAS_CHOICES = [
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
    ('ambos', 'Sábado y Domingo'),
]

BEBIDAS_PRINCIPALES = [
    ('agua', 'Agua'),
    ('vino', 'Vino'),
    ('cerveza', 'Cerveza'),
    ('tinto_verano', 'Tinto de Verano'),
    ('rebujito', 'Rebujito'),
]

BEBIDAS_ALCOHOL = [
    ('ron_barcelo', 'Ron Barceló'),
    ('ron_legendario', 'Ron Legendario'),
    ('whisky_dyc8', 'Whisky Dyc8'),
    ('whisky_red', 'Whisky Red Label'),
    ('ginebra_larios', 'Ginebra Larios'),
    ('ginebra_beefeater', 'Ginebra Beefeater'),
    ('vodka', 'Vodka'),
    ('ninguno', 'Ninguno'),
]

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    bebida_principal = models.CharField(
        max_length=20,
        choices=BEBIDAS_PRINCIPALES,
        default='agua'
    )
    refresco = models.CharField(max_length=100, blank=True, null=True)
    alcohol = models.CharField(
        max_length=20,
        choices=BEBIDAS_ALCOHOL,
        default='ninguno'
    )
    dias = models.CharField(
        max_length=10,
        choices=DIAS_CHOICES,
        default='sabado'
    )
    ha_pagado = models.BooleanField(default=False)
    cantidad_pagar = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
