from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from .models import Persona
from .forms import PersonaForm

# Vista de lista de personas
@login_required(login_url='login')
def persona_list(request):
    personas = Persona.objects.all()
    
    # Búsqueda por nombre o apellidos
    search = request.GET.get('search', '')
    if search:
        personas = personas.filter(Q(nombre__icontains=search) | Q(apellidos__icontains=search))
    
    # Filtro por estado de pago
    ha_pagado = request.GET.get('ha_pagado', '')
    if ha_pagado:
        personas = personas.filter(ha_pagado=ha_pagado == 'true')
    
    # Filtro por día
    dias = request.GET.get('dias', '')
    if dias:
        personas = personas.filter(dias=dias)
    
    # Filtro por bebida principal
    bebida_principal = request.GET.get('bebida_principal', '')
    if bebida_principal:
        personas = personas.filter(bebida_principal=bebida_principal)
    
    context = {
        'personas': personas,
        'total_personas': personas.count(),
        'search': search,
        'ha_pagado': ha_pagado,
        'dias': dias,
        'bebida_principal': bebida_principal,
    }
    return render(request, 'personas/persona_list.html', context)

# Vista para crear/editar persona
@login_required(login_url='login')
def persona_form(request, pk=None):
    if pk:
        persona = get_object_or_404(Persona, pk=pk)
        titulo = "Editar Persona"
    else:
        persona = None
        titulo = "Añadir Persona"
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('persona_list')
    else:
        form = PersonaForm(instance=persona)
    
    context = {
        'form': form,
        'titulo': titulo,
        'persona': persona,
    }
    return render(request, 'personas/persona_form.html', context)

# Vista de detalle de persona
@login_required(login_url='login')
def persona_detail(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    context = {
        'persona': persona,
    }
    return render(request, 'personas/persona_detail.html', context)

# Vista de análisis
@login_required(login_url='login')
def analytics(request):
    todas_personas = Persona.objects.all()
    
    # Estadísticas generales
    total_personas = todas_personas.count()
    total_pagado = todas_personas.filter(ha_pagado=True).count()
    total_no_pagado = todas_personas.filter(ha_pagado=False).count()
    
    # Cantidad total a pagar
    cantidad_total = todas_personas.aggregate(Sum('cantidad_pagar'))['cantidad_pagar__sum'] or 0
    cantidad_pagada = todas_personas.filter(ha_pagado=True).aggregate(Sum('cantidad_pagar'))['cantidad_pagar__sum'] or 0
    cantidad_pendiente = cantidad_total - cantidad_pagada
    
    # Análisis por día
    personas_sabado = todas_personas.filter(Q(dias='sabado') | Q(dias='ambos')).count()
    personas_domingo = todas_personas.filter(Q(dias='domingo') | Q(dias='ambos')).count()
    
    # Análisis de bebidas principales
    bebidas_principales = todas_personas.values('bebida_principal').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Análisis de bebidas alcohólicas
    bebidas_alcohol = todas_personas.values('alcohol').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Personas por estado de pago
    pagadas = todas_personas.filter(ha_pagado=True)
    no_pagadas = todas_personas.filter(ha_pagado=False)
    
    context = {
        'total_personas': total_personas,
        'total_pagado': total_pagado,
        'total_no_pagado': total_no_pagado,
        'cantidad_total': cantidad_total,
        'cantidad_pagada': cantidad_pagada,
        'cantidad_pendiente': cantidad_pendiente,
        'personas_sabado': personas_sabado,
        'personas_domingo': personas_domingo,
        'bebidas_principales': bebidas_principales,
        'bebidas_alcohol': bebidas_alcohol,
        'pagadas': pagadas,
        'no_pagadas': no_pagadas,
    }
    return render(request, 'personas/analytics.html', context)

# Vista de lista de compra
@login_required(login_url='login')
def shopping_list(request):
    personas = Persona.objects.all()
    
    # Contar bebidas principales (1 en 1, sin multiplicar)
    bebidas_principales_count = {}
    for persona in personas:
        if persona.bebida_principal not in bebidas_principales_count:
            bebidas_principales_count[persona.bebida_principal] = 0
        bebidas_principales_count[persona.bebida_principal] += 1
    
    # Contar refrescos (x2 si asiste ambos días)
    refrescos_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.refresco:
            if persona.refresco not in refrescos_count:
                refrescos_count[persona.refresco] = 0
            refrescos_count[persona.refresco] += multiplicador
    
    # Contar bebidas alcohólicas (x2 si asiste ambos días)
    bebidas_alcohol_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.alcohol != 'ninguno':
            if persona.alcohol not in bebidas_alcohol_count:
                bebidas_alcohol_count[persona.alcohol] = 0
            bebidas_alcohol_count[persona.alcohol] += multiplicador
    
    context = {
        'bebidas_principales': bebidas_principales_count,
        'refrescos': refrescos_count,
        'bebidas_alcohol': bebidas_alcohol_count,
        'total_personas': personas.count(),
    }
    return render(request, 'personas/shopping_list.html', context)
