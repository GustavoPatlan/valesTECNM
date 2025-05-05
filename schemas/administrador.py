from dotenv import load_dotenv
from config.database import obtenerDatosDB_Varios_Descarga
import os, re, json
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from io import BytesIO
from config.database import obtenerDatosDB_Varios_Descarga
from datetime import datetime

lab_material = {
        'Y1-Y2': "labpotencia",
        'Y6-Y7': "labelectronica",
        'Y8': "labthird"
    }

load_dotenv(dotenv_path="config/.env")

# Lista de carreras profesionales disponibles en el instituto.
carreras_disponibles = os.getenv("CARRERAS_DISPONIBLES").split(",") if os.getenv("CARRERAS_DISPONIBLES") else []

def validar_correo(correo, identificador):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    patron = rf"^[a-zA-Z]?[0-9]*{re.escape(identificador)}@morelia\.tecnm\.mx$"
    return re.match(patron, correo) is not None

def generarListadeEstudiantesPDF():
    # Obtener datos de la base de datos.
    sql = "SELECT ncontrol, correo, carrera, nombres, apellidos FROM usuarios"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Número de Control", "Correo", "Carrera", "Nombres", "Apellidos"]

    # Prepara el buffer PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para cabeceras de tabla
    style_header = ParagraphStyle(
        'header',
        parent=styles['Normal'],
        fontSize=3,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1  # Centrado
    )
    
    # Estilo para datos normales
    style_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=5,
        leading=10,
        fontName='Helvetica',
        wordWrap='CJK'
    )

    content = []

    # Título y fecha
    content.append(Paragraph(f"Estudiantes valesTECNM", styles['Title']))
    content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Procesamos los datos
    all_tables = []
    
    # Definir anchos de columnas proporcionales
    col_widths = [50, 140, 160, 100, 100]
    
    # Cabecera de la tabla
    header_row = [Paragraph(col.upper(), style_header) for col in columnas[:-2]]  # Excluimos reporte y materiales
    all_tables.append(header_row)
    
    for fila in datos:
        main_data = []
        for item in fila:  # Excluimos las columnas de reporte e i_material
            text = str(item)
            main_data.append(Paragraph(text, style_normal))
        all_tables.append(main_data)
    # Crear la tabla principal
    tabla = Table(all_tables, colWidths=col_widths)
    
    # Estilo de la tabla
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c336c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')),
    ]

    tabla.setStyle(TableStyle(table_styles))

    content.append(tabla)

    # Pie de página profesional
    def agregar_pie(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#4F81BD'))
        canvas.drawString(40, 20, "Sistema de Control de Laboratorios")
        canvas.drawRightString(doc.width + doc.leftMargin - 40, 20, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(content, onFirstPage=agregar_pie, onLaterPages=agregar_pie)
    buffer.seek(0)
    return buffer

def generarListadeEstudiantesCSV():
    # Obtener datos de la base de datos.
    sql = "SELECT * FROM usuarios"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Número de Control", "Correo", "Carrera", "Nombres", "Apellidos", "Contraseña"]

    # Producir el contenido CSV línea por línea.
    yield '\ufeff' + ','.join(columnas) + '\n'

    for fila in datos:
        fila = list(fila)
        fila_limpia = [str(col).replace('\n', ' ').replace(',', ';') for col in fila]
        yield ','.join(fila_limpia) + '\n'

def generarListadeMaestrosPDF():
    # Obtener datos de la base de datos.
    sql = "SELECT * FROM maestros"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Identificación", "Correo", "Nombres", "Apellidos", "Contraseña"]

    # Prepara el buffer PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para cabeceras de tabla
    style_header = ParagraphStyle(
        'header',
        parent=styles['Normal'],
        fontSize=3,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1  # Centrado
    )
    
    # Estilo para datos normales
    style_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=5,
        leading=10,
        fontName='Helvetica',
        wordWrap='CJK'
    )

    content = []

    # Título y fecha
    content.append(Paragraph(f"Maestros valesTECNM", styles['Title']))
    content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Procesamos los datos
    all_tables = []
    
    # Definir anchos de columnas proporcionales
    col_widths = [50, 160, 100, 100, 50]
    
    # Cabecera de la tabla
    header_row = [Paragraph(col.upper(), style_header) for col in columnas[:-2]]  # Excluimos reporte y materiales
    all_tables.append(header_row)
    
    for fila in datos:
        main_data = []
        for item in fila:  # Excluimos las columnas de reporte e i_material
            text = str(item)
            main_data.append(Paragraph(text, style_normal))
        all_tables.append(main_data)
    # Crear la tabla principal
    tabla = Table(all_tables, colWidths=col_widths)
    
    # Estilo de la tabla
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c336c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')),
    ]

    tabla.setStyle(TableStyle(table_styles))

    content.append(tabla)

    # Pie de página profesional
    def agregar_pie(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#4F81BD'))
        canvas.drawString(40, 20, "Sistema de Control de Laboratorios")
        canvas.drawRightString(doc.width + doc.leftMargin - 40, 20, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(content, onFirstPage=agregar_pie, onLaterPages=agregar_pie)
    buffer.seek(0)
    return buffer

def generarListadeMaestrosCSV():
    # Obtener datos de la base de datos.
    sql = "SELECT id, correo, nombres, apellidos FROM maestros"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Identificación", "Correo", "Nombres", "Apellidos"]

    # Producir el contenido CSV línea por línea.
    yield '\ufeff' + ','.join(columnas) + '\n'

    for fila in datos:
        fila = list(fila)
        fila_limpia = [str(col).replace('\n', ' ').replace(',', ';') for col in fila]
        yield ','.join(fila_limpia) + '\n'

def generarListadeCaseterosPDF():
    # Obtener datos de la base de datos.
    sql = "SELECT * FROM caseteros"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Identificación", "Nombres", "Apellidos", "Laboratorio", "Correo", "Contraseña"]

    # Prepara el buffer PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para cabeceras de tabla
    style_header = ParagraphStyle(
        'header',
        parent=styles['Normal'],
        fontSize=3,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1  # Centrado
    )
    
    # Estilo para datos normales
    style_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=5,
        leading=10,
        fontName='Helvetica',
        wordWrap='CJK'
    )

    content = []

    # Título y fecha
    content.append(Paragraph(f"Caseteros valesTECNM", styles['Title']))
    content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Procesamos los datos
    all_tables = []
    
    # Definir anchos de columnas proporcionales
    col_widths = [50, 100, 100, 50, 160, 50]
    
    # Cabecera de la tabla
    header_row = [Paragraph(col.upper(), style_header) for col in columnas[:-2]]  # Excluimos reporte y materiales
    all_tables.append(header_row)
    
    for fila in datos:
        main_data = []
        for item in fila:  # Excluimos las columnas de reporte e i_material
            text = str(item)
            main_data.append(Paragraph(text, style_normal))
        all_tables.append(main_data)
    # Crear la tabla principal
    tabla = Table(all_tables, colWidths=col_widths)
    
    # Estilo de la tabla
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c336c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')),
    ]

    tabla.setStyle(TableStyle(table_styles))

    content.append(tabla)

    # Pie de página profesional
    def agregar_pie(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#4F81BD'))
        canvas.drawString(40, 20, "Sistema de Control de Laboratorios")
        canvas.drawRightString(doc.width + doc.leftMargin - 40, 20, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(content, onFirstPage=agregar_pie, onLaterPages=agregar_pie)
    buffer.seek(0)
    return buffer

def generarListadeCaseterosCSV():
    # Obtener datos de la base de datos.
    sql = "SELECT * FROM caseteros"
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = ["Identificación", "Nombres", "Apellidos", "Laboratorio", "Correo", "Contraseña"]

    # Producir el contenido CSV línea por línea.
    yield '\ufeff' + ','.join(columnas) + '\n'

    for fila in datos:
        fila = list(fila)
        fila_limpia = [str(col).replace('\n', ' ').replace(',', ';') for col in fila]
        yield ','.join(fila_limpia) + '\n'

def generarListaMaterialesCSV(laboratorio):
    """
    Genera un archivo CSV con el inventario completo de materiales de un laboratorio específico.
    El archivo está optimizado para su visualización en Excel y otras hojas de cálculo.

    Parámetros:
        laboratorio: Nombre del laboratorio del cual se generará el reporte.
    """
    condition = lab_material.get(laboratorio)

    # Obtener datos de la base de datos.
    sql = f"""
            SELECT 
                EQUIPO, MARCA, MODELO, N_CASETA, N_SERIE,
                N_INVENTARIO, VOLTAJE, POTENCIA, CANTIDAD,
                NUMERACION, OBSERVACIONES
            FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC
            """
    datos = obtenerDatosDB_Varios_Descarga(sql)

    # Definir encabezados de columnas.
    columnas = [
        "Equipo", "Marca", "Modelo", "Caseta", "N. Serie","N. Inventario", 
        "Voltaje", "Potencia", "Cantidad", "Numeracion", "Observaciones"
    ]

    # Producir el contenido CSV línea por línea.
    yield '\ufeff' + ','.join(columnas) + '\n'

    for fila in datos:
        fila = list(fila)
        fila_limpia = [str(col).replace('\n', ' ').replace(',', ';') for col in fila]
        yield ','.join(fila_limpia) + '\n'

def generarMaterialesPDF(laboratorio):
    """
    Genera un reporte PDF profesional del inventario de materiales de un laboratorio específico.

    Parámetros:
        laboratorio: Nombre del laboratorio para el cual se generará el reporte.

    Retorna:
        BytesIO: Buffer con el archivo PDF generado listo para descargar.

    Características del PDF:
        - Formato horizontal (A4 landscape).
        - Diseño profesional con estilos personalizados.
        - Incluye todos los campos de inventario.
        - Observaciones integradas como filas combinadas.
        - Encabezado y pie de página estilizados.
        - Ordenamiento por numeración y equipo.
    """
    condition = lab_material.get(laboratorio)
    # Obtener datos de la base de datos
    sql = f"""
            SELECT 
                EQUIPO, MARCA, MODELO, N_CASETA, N_SERIE,
                N_INVENTARIO, VOLTAJE, POTENCIA, CANTIDAD,
                NUMERACION, OBSERVACIONES
            FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC
            """
    datos = obtenerDatosDB_Varios_Descarga(sql)

    columnas = [
        "Equipo", "Marca", "Modelo", "Caseta", "N. Serie","N. Inventario", 
        "Voltaje", "Potencia", "Cantidad", "Numeracion"
    ]

    # Prepara el buffer PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para cabeceras de tabla
    style_header = ParagraphStyle(
        'header',
        parent=styles['Normal'],
        fontSize=3,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1  # Centrado
    )
    
    # Estilo para datos normales
    style_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=5,
        leading=10,
        fontName='Helvetica',
        wordWrap='CJK'
    )

    content = []

    # Título y fecha
    content.append(Paragraph(f"Materiales - {laboratorio}", styles['Title']))
    content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Procesamos los datos
    all_tables = []
    
    # Definir anchos de columnas proporcionales
    col_widths = [60, 40, 50, 40, 80, 80, 40, 40, 30, 30]
    
    # Cabecera de la tabla
    header_row = [Paragraph(col.upper(), style_header) for col in columnas]  # Excluimos reporte y materiales
    all_tables.append(header_row)
    
    for fila in datos:
        main_data = []
        for item in fila[:-1]:
            text = str(item)
            main_data.append(Paragraph(text, style_normal))
        all_tables.append(main_data)

        # Fila de reporte - abarca todas las columnas
        reporte_text = f"<b>OBSERVACIONES:</b> {fila[-1]}"
        reporte_paragraph = Paragraph(reporte_text, style_normal)
        reporte_row = [reporte_paragraph] + [''] * (len(col_widths) - 1)  # solo la primera celda con texto
        all_tables.append(reporte_row)

    # Crear la tabla principal
    tabla = Table(all_tables, colWidths=col_widths)
    
    # Estilo de la tabla
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c336c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')),
    ]

    # Detectamos las filas de reporte para hacerles SPAN
    for i in range(1, len(all_tables)):
        if all_tables[i][1:] == [''] * (len(col_widths) - 1):  # solo la primera celda con texto
            table_styles.append(('SPAN', (0, i), (-1, i)))

    tabla.setStyle(TableStyle(table_styles))

    content.append(tabla)

    # Pie de página profesional
    def agregar_pie(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#4F81BD'))
        canvas.drawString(40, 20, "Sistema de Control de Laboratorios")
        canvas.drawRightString(doc.width + doc.leftMargin - 40, 20, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(content, onFirstPage=agregar_pie, onLaterPages=agregar_pie)
    buffer.seek(0)
    return buffer