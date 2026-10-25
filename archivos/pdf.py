import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generar_pdf_presupuesto(cabecera, detalles):
    """
    Genera un comprobante PDF del presupuesto con la estética de Tornería Gonzales.
    `cabecera`: dict con keys ('id_presupuesto' o 'id', 'fecha', 'cliente', 'descripcion', 'mano_obra', 'total_materiales', 'total_general')
    `detalles`: list de dicts con keys ('nombre', 'cantidad', 'unidad', 'precio_venta', 'subtotal')
    """
    id_presu = cabecera.get("id_presupuesto", cabecera.get("id", 1))
    nombre_archivo = f"Presupuesto_{id_presu}.pdf"
    
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Estilos de texto personalizados
    style_empresa_titulo = ParagraphStyle(
        'EmpresaTitulo',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#003366')
    )
    
    style_empresa_sub = ParagraphStyle(
        'EmpresaSub',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#444444')
    )

    style_presu_titulo = ParagraphStyle(
        'PresuTitulo',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=2, # Derecha
        textColor=colors.HexColor('#003366')
    )

    style_presu_meta = ParagraphStyle(
        'PresuMeta',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=2, # Derecha
        textColor=colors.HexColor('#333333')
    )

    style_seccion_hdr = ParagraphStyle(
        'SeccionHdr',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#003366')
    )

    style_body = ParagraphStyle(
        'BodyNormal',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#222222')
    )

    style_th = ParagraphStyle(
        'TablaHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#003366')
    )

    style_td_right = ParagraphStyle(
        'TablaCellRight',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        alignment=2,
        textColor=colors.HexColor('#222222')
    )

    story = []

    # ---------------------------------------------------------
    # 1. ENCABEZADO (DATOS EMPRESA + NÚMERO Y FECHA)
    # ---------------------------------------------------------
    col1 = [
        Paragraph("TORNERÍA GONZALES", style_empresa_titulo),
        Paragraph("Trabajos de Mecanizado y Tornería", style_empresa_sub),
        Paragraph("Teléfono: (3537) - Taller", style_empresa_sub),
        Paragraph("Email: contacto@torneriagonzales.com", style_empresa_sub),
    ]

    fecha_val = cabecera.get("fecha", "")
    col2 = [
        Paragraph("PRESUPUESTO", style_presu_titulo),
        Spacer(1, 4),
        Paragraph(f"FECHA: {fecha_val}", style_presu_meta),
        Paragraph(f"PRESUPUESTO NÚMERO<br/>#{id_presu}", style_presu_meta),
    ]

    tbl_header = Table([[col1, col2]], colWidths=[4.25 * inch, 3.25 * inch])
    tbl_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(tbl_header)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # 2. SECCIÓN CLIENTE Y TRABAJO
    # ---------------------------------------------------------
    cliente_val = cabecera.get("cliente", "")
    trabajo_val = cabecera.get("descripcion", "")

    col_cli = [
        Paragraph("PRESUPUESTAR A:", style_seccion_hdr),
        Paragraph(f"<b>Cliente:</b> {cliente_val}", style_body),
        Paragraph(f"<b>Trabajo:</b> {trabajo_val}", style_body),
    ]

    tbl_cliente = Table([[col_cli]], colWidths=[7.5 * inch])
    tbl_cliente.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(tbl_cliente)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # 3. TABLA DE DETALLES (MATERIALES Y SERVICIOS)
    # ---------------------------------------------------------
    tabla_datos = [
        [
            Paragraph("DESCRIPCIÓN", style_th),
            Paragraph("CANTIDAD", style_th),
            Paragraph("PRECIO UNIT.", ParagraphStyle('RHeader', parent=style_th, alignment=2)),
            Paragraph("TOTAL", ParagraphStyle('RHeader', parent=style_th, alignment=2))
        ]
    ]

    for item in detalles:
        nombre = item.get("nombre", "")
        unidad = item.get("unidad", "")
        cant = item.get("cantidad", 0.0)
        precio = item.get("precio_venta", 0.0)
        subtotal = item.get("subtotal", cant * precio)

        cant_str = f"{cant:.2f} {unidad}".strip()
        precio_str = f"$ {precio:.2f}"
        sub_str = f"$ {subtotal:.2f}"

        tabla_datos.append([
            Paragraph(nombre, style_body),
            Paragraph(cant_str, style_body),
            Paragraph(precio_str, style_td_right),
            Paragraph(sub_str, style_td_right),
        ])

    tbl_detalles = Table(tabla_datos, colWidths=[3.5 * inch, 1.25 * inch, 1.35 * inch, 1.4 * inch])
    tbl_detalles.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9E1F2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
    ]))
    story.append(tbl_detalles)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # 4. RESUMEN DE TOTALES (SUBTOTAL, MANO DE OBRA, TOTAL)
    # ---------------------------------------------------------
    subtotal_mat = cabecera.get("total_materiales", 0.0)
    mano_obra = cabecera.get("mano_obra", 0.0)
    total_gen = cabecera.get("total_general", subtotal_mat + mano_obra)

    totales_datos = [
        [
            Paragraph("SUBTOTAL MATERIALES:", ParagraphStyle('TLbl', parent=style_seccion_hdr, alignment=2)),
            Paragraph(f"$ {subtotal_mat:.2f}", style_td_right)
        ],
        [
            Paragraph("MANO DE OBRA:", ParagraphStyle('TLbl', parent=style_seccion_hdr, alignment=2)),
            Paragraph(f"$ {mano_obra:.2f}", style_td_right)
        ],
        [
            Paragraph("TOTAL GENERAL:", ParagraphStyle('TLblBold', parent=style_seccion_hdr, alignment=2, fontSize=11)),
            Paragraph(f"<b>$ {total_gen:.2f}</b>", ParagraphStyle('TRightBold', parent=style_td_right, fontSize=11))
        ]
    ]

    tbl_totales = Table(totales_datos, colWidths=[5.8 * inch, 1.7 * inch])
    tbl_totales.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#003366')),
    ]))
    story.append(tbl_totales)
    story.append(Spacer(1, 30))

    # ---------------------------------------------------------
    # 5. PIE DE PÁGINA / AGRADECIMIENTO
    # ---------------------------------------------------------
    style_gracias = ParagraphStyle(
        'Gracias',
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=1, # Centrado
        textColor=colors.HexColor('#003366')
    )
    story.append(Paragraph("GRACIAS POR SU CONFIANZA", style_gracias))

    # Construir el PDF
    doc.build(story)
    return nombre_archivo