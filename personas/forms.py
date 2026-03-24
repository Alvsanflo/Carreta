from django import forms
from .models import Persona, StockAlcohol, StockDinero


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'bebida_principal', 'refresco',
                  'alcohol', 'dias', 'ha_pagado', 'cantidad_pagar']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'bebida_principal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'refresco': forms.Select(attrs={
                'class': 'form-control'
            }),
            'alcohol': forms.Select(attrs={
                'class': 'form-control'
            }),
            'dias': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ha_pagado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'cantidad_pagar': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }


class StockAlcoholForm(forms.ModelForm):
    class Meta:
        model = StockAlcohol
        fields = ['bebida', 'cantidad_stock']
        widgets = {
            'bebida': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }


class StockDineroForm(forms.ModelForm):
    class Meta:
        model = StockDinero
        fields = ['concepto', 'cantidad', 'tipo']
        widgets = {
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Concepto del movimiento'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }
