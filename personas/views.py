from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from .models import Persona, StockAlcohol, StockDinero, BEBIDAS_ALCOHOL, REFRESCOS_CHOICES, BEBIDAS_PRINCIPALES
from .forms import PersonaForm, StockAlcoholForm, StockDineroForm
import io

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

    # Dict para nombres legibles
    alcohol_display = dict(BEBIDAS_ALCOHOL)
    refresco_display = dict(REFRESCOS_CHOICES)
    principal_display = dict(BEBIDAS_PRINCIPALES)

    # Contar bebidas principales
    bebidas_principales_count = {}
    for persona in personas:
        display = principal_display.get(persona.bebida_principal, persona.bebida_principal)
        if display not in bebidas_principales_count:
            bebidas_principales_count[display] = 0
        bebidas_principales_count[display] += 1

    # Contar refrescos (x2 si asiste ambos días)
    refrescos_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.refresco and persona.refresco != 'ninguno':
            display = refresco_display.get(persona.refresco, persona.refresco)
            if display not in refrescos_count:
                refrescos_count[display] = 0
            refrescos_count[display] += multiplicador

    # Contar bebidas alcohólicas (x2 si asiste ambos días)
    bebidas_alcohol_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.alcohol != 'ninguno':
            display = alcohol_display.get(persona.alcohol, persona.alcohol)
            if display not in bebidas_alcohol_count:
                bebidas_alcohol_count[display] = 0
            bebidas_alcohol_count[display] += multiplicador

    # Stock de alcohol
    stock_alcohol = StockAlcohol.objects.all()

    context = {
        'bebidas_principales': bebidas_principales_count,
        'refrescos': refrescos_count,
        'bebidas_alcohol': bebidas_alcohol_count,
        'total_personas': personas.count(),
        'stock_alcohol': stock_alcohol,
    }
    return render(request, 'personas/shopping_list.html', context)


# PDF de la lista de compra
@login_required(login_url='login')
def shopping_list_pdf(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    personas = Persona.objects.all()
    alcohol_display = dict(BEBIDAS_ALCOHOL)
    refresco_display = dict(REFRESCOS_CHOICES)
    principal_display = dict(BEBIDAS_PRINCIPALES)

    # Calcular datos
    bebidas_principales_count = {}
    for persona in personas:
        display = principal_display.get(persona.bebida_principal, persona.bebida_principal)
        bebidas_principales_count[display] = bebidas_principales_count.get(display, 0) + 1

    refrescos_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.refresco and persona.refresco != 'ninguno':
            display = refresco_display.get(persona.refresco, persona.refresco)
            refrescos_count[display] = refrescos_count.get(display, 0) + multiplicador

    bebidas_alcohol_count = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.alcohol != 'ninguno':
            display = alcohol_display.get(persona.alcohol, persona.alcohol)
            bebidas_alcohol_count[display] = bebidas_alcohol_count.get(display, 0) + multiplicador

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=22, textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20
    )
    elements.append(Paragraph('Lista de Compra - Carreta Romería', title_style))
    elements.append(Paragraph(f'Total personas: {personas.count()}', styles['Normal']))
    elements.append(Spacer(1, 20))

    header_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'],
        fontSize=14, textColor=colors.HexColor('#4facfe'),
        spaceAfter=10
    )

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4facfe')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])

    # Bebidas principales
    if bebidas_principales_count:
        elements.append(Paragraph('Bebidas Principales', header_style))
        data = [['Bebida', 'Cantidad']]
        for bebida, cantidad in bebidas_principales_count.items():
            data.append([bebida, str(cantidad)])
        t = Table(data, colWidths=[10*cm, 5*cm])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 20))

    # Refrescos
    if refrescos_count:
        elements.append(Paragraph('Refrescos', header_style))
        data = [['Refresco', 'Cantidad']]
        for refresco, cantidad in refrescos_count.items():
            data.append([refresco, str(cantidad)])
        t = Table(data, colWidths=[10*cm, 5*cm])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 20))

    # Bebidas alcohólicas
    if bebidas_alcohol_count:
        elements.append(Paragraph('Bebidas Alcohólicas', header_style))
        data = [['Bebida', 'Cantidad']]
        for alcohol, cantidad in bebidas_alcohol_count.items():
            data.append([alcohol, str(cantidad)])
        t = Table(data, colWidths=[10*cm, 5*cm])
        t.setStyle(table_style)
        elements.append(t)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_compra_carreta.pdf"'
    return response


# Vista de stock
@login_required(login_url='login')
def stock_view(request):
    stock_alcohol = StockAlcohol.objects.all()
    movimientos = StockDinero.objects.all()

    total_ingresos = movimientos.filter(tipo='ingreso').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    total_gastos = movimientos.filter(tipo='gasto').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    saldo = total_ingresos - total_gastos

    # Calcular necesidades de alcohol vs stock
    personas = Persona.objects.all()
    alcohol_display = dict(BEBIDAS_ALCOHOL)
    necesidades_alcohol = {}
    for persona in personas:
        multiplicador = 2 if persona.dias == 'ambos' else 1
        if persona.alcohol != 'ninguno':
            if persona.alcohol not in necesidades_alcohol:
                necesidades_alcohol[persona.alcohol] = 0
            necesidades_alcohol[persona.alcohol] += multiplicador

    stock_comparison = []
    for stock_item in stock_alcohol:
        necesario = necesidades_alcohol.get(stock_item.bebida, 0)
        stock_comparison.append({
            'bebida': stock_item.get_bebida_display(),
            'stock': stock_item.cantidad_stock,
            'necesario': necesario,
            'diferencia': stock_item.cantidad_stock - necesario,
            'stock_id': stock_item.pk,
        })

    # Forms
    alcohol_form = StockAlcoholForm()
    dinero_form = StockDineroForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_alcohol':
            alcohol_form = StockAlcoholForm(request.POST)
            if alcohol_form.is_valid():
                bebida = alcohol_form.cleaned_data['bebida']
                cantidad = alcohol_form.cleaned_data['cantidad_stock']
                obj, created = StockAlcohol.objects.get_or_create(
                    bebida=bebida,
                    defaults={'cantidad_stock': cantidad}
                )
                if not created:
                    obj.cantidad_stock = cantidad
                    obj.save()
                return redirect('stock')
        elif action == 'add_dinero':
            dinero_form = StockDineroForm(request.POST)
            if dinero_form.is_valid():
                dinero_form.save()
                return redirect('stock')
        elif action == 'delete_alcohol':
            stock_id = request.POST.get('stock_id')
            StockAlcohol.objects.filter(pk=stock_id).delete()
            return redirect('stock')
        elif action == 'delete_dinero':
            mov_id = request.POST.get('mov_id')
            StockDinero.objects.filter(pk=mov_id).delete()
            return redirect('stock')

    context = {
        'stock_alcohol': stock_alcohol,
        'stock_comparison': stock_comparison,
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'saldo': saldo,
        'alcohol_form': alcohol_form,
        'dinero_form': dinero_form,
    }
    return render(request, 'personas/stock.html', context)
