from django import forms
from .models import Persona, StockAlcohol, StockDinero, StockObjeto, BEBIDAS_PRINCIPALES


class PersonaForm(forms.ModelForm):
    bebida_principal = forms.MultipleChoiceField(
        choices=BEBIDAS_PRINCIPALES,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        required=True,
        label='Bebida Principal'
    )

    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'bebida_principal',
                  'refresco', 'alcohol', 'dias', 'ha_pagado', 'cantidad_pagar']
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.bebida_principal:
            self.initial['bebida_principal'] = [
                v.strip() for v in self.instance.bebida_principal.split(',') if v.strip()
            ]

    def clean_bebida_principal(self):
        bebidas = self.cleaned_data.get('bebida_principal', [])
        if not bebidas:
            raise forms.ValidationError('Selecciona al menos una bebida principal.')
        return bebidas

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.bebida_principal = ','.join(self.cleaned_data['bebida_principal'])
        if commit:
            instance.save()
        return instance


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


class StockObjetoForm(forms.ModelForm):
    class Meta:
        model = StockObjeto
        fields = ['objeto', 'persona']
        widgets = {
            'objeto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Objeto'
            }),
            'persona': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['persona'].required = False
        self.fields['persona'].empty_label = 'Selecciona persona'
        self.fields['persona'].queryset = Persona.objects.order_by('nombre', 'apellidos')
