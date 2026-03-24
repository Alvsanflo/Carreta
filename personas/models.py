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

REFRESCOS_CHOICES = [
    ('coca_cola', 'Coca-Cola'),
    ('coca_cola_zero', 'Coca-Cola cero'),
    ('coca_cola_zero_zero', 'Coca-Cola cero cero'),
    ('fanta_naranja', 'Fanta Naranja'),
    ('fanta_limon', 'Fanta Limón'),
    ('sprite', 'Sprite'),
    ('aquarius', 'Aquarius'),
    ('tonica', 'Tónica'),
    ('nestea', 'Nestea'),
    ('ninguno', 'Ninguno'),
]

BEBIDAS_ALCOHOL = [
    ('ron_barcelo', 'Ron Barceló'),
    ('ron_legendario', 'Ron Legendario'),
    ('whisky_dyc8', 'Whisky Dyc8'),
    ('whisky_red', 'Whisky Red Label'),
    ('ginebra_larios', 'Ginebra Larios'),
    ('ginebra_beefeater', 'Ginebra Beefeater'),
    ('ginebra_exotic', 'Ginebra Exotic'),
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
    refresco = models.CharField(
        max_length=20,
        choices=REFRESCOS_CHOICES,
        default='ninguno'
    )
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


class StockAlcohol(models.Model):
    bebida = models.CharField(
        max_length=20,
        choices=[c for c in BEBIDAS_ALCOHOL if c[0] != 'ninguno'],
        unique=True
    )
    cantidad_stock = models.IntegerField(default=0, verbose_name="Botellas en stock")

    class Meta:
        verbose_name = "Stock de Alcohol"
        verbose_name_plural = "Stock de Alcohol"

    def __str__(self):
        return f"{self.get_bebida_display()} - {self.cantidad_stock} uds"


class StockDinero(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    concepto = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='ingreso')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Movimiento de Dinero"
        verbose_name_plural = "Movimientos de Dinero"

    def __str__(self):
        signo = '+' if self.tipo == 'ingreso' else '-'
        return f"{signo}{self.cantidad}€ - {self.concepto}"
