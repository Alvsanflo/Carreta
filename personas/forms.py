from django import forms
from .models import Persona

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
            'refresco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Coca-Cola, Sprite...'
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
