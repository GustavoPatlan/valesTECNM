from collections import defaultdict
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from io import BytesIO
from config.database import obtenerDatosDB_Varios_Descarga
from datetime import datetime
import json

lab_conditions = {
        'Y1-Y2': "laboratory = 'Y1' OR laboratory = 'Y2'",
        'Y6-Y7': "laboratory = 'Y6' OR laboratory = 'Y7'",
        'Y8': "laboratory = 'Y8'"
    }

lab_material = {
        'Y1-Y2': "labpotencia",
        'Y6-Y7': "labelectronica",
        'Y8': "labthird"
    }

def crearListadeEquipo(equipos):
    """
    Transforma una lista de tuplas (equipo, identificacion) en una lista de diccionarios
    donde cada clave es un equipo y su valor es la lista de identificaciones asociadas.
    """
    agrupados = defaultdict(list)
    for equipo, identificacion in equipos:
        agrupados[equipo].append(identificacion)
    resultado = [{k: v} for k, v in agrupados.items()]
    return resultado

def obtener_horario():
    """
    Obtiene la fecha y hora actual del sistema formateadas para visualización.

    Genera:
        - Fecha en formato DD/MM/AAAA.
        - Hora en formato 12 horas con indicador AM/PM.
        - Los datos se retornan como una lista.

    Resultado:
        resultado: Datos del con fecha y hora.
    """
    ahora = datetime.now()
    fecha = ahora.strftime('%d/%m/%Y')
    hora = ahora.strftime('%I:%M')
    periodo = 'AM' if ahora.hour < 12 else 'PM'
    hora_con_periodo = f"{hora} {periodo}"
    datos = [fecha, hora_con_periodo]
    return datos

def crear_identificacion(ncontrol, vale, horarios):
    """
    Genera un identificador único para vales de préstamo basado en:
        - Tipo de vale (PROYECTO, MAESTRO o LABORATORIO).
        - Número de control del solicitante.
        - Fecha y hora actual.
    """
    if vale == 'PROYECTO':
        lada = 'P'
    elif vale == 'MAESTRO':
        lada = 'M'
    else:
        lada = 'L'
    identificacion = lada + ncontrol + horarios[1].replace(" ", "").replace(":", "") + horarios[0].replace("/", "") 
    return identificacion

def generarListaCSV(laboratorio):
    """
    Genera un archivo CSV con el historial completo de préstamos de un laboratorio específico,
    formateado para óptima compatibilidad con Excel y otros sistemas.

    Parámetros:
        laboratorio: Nombre del laboratorio para generar el reporte.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"""
            SELECT 
                ncontrol, hora_solicitud, fecha_solicitud, hora_final, fecha_final,
                name, lastname, teacher, casetero, topic, grupo, number_group,
                laboratory, tipo_vale, reporte, i_material
            FROM registro
            WHERE ({condition})
            ORDER BY fecha_final ASC
            """
    datos = obtenerDatosDB_Varios_Descarga(sql)

    columnas = [
        "Identificación", "Hora Solicitud", "Fecha Solicitud", "Hora Final", "Fecha Final",
        "Nombre", "Apellido", "Profesor", "Casetero", "Tema", "Grupo", "No. Grupo",
        "Laboratorio", "Vale", 'Reporte', 'Materiales'
    ]

    # BOM UTF-8 para compatibilidad con Excel
    yield '\ufeff' + ','.join(columnas) + '\n'

    for fila in datos:
        fila = list(fila)
        try:
            materiales = json.loads(fila[-1])  # Asumimos que i_material es la última columna
            texto_materiales = ' | '.join(f"{item[0]}: {item[1]}" for item in materiales)
            fila[-1] = texto_materiales
        except Exception as e:
            fila[-1] = f"Error JSON: {e}"

        fila_limpia = [str(col).replace('\n', ' ').replace(',', ';') for col in fila]
        yield ','.join(fila_limpia) + '\n'

def generarListaPDF(laboratorio):
    """
    Genera un reporte PDF profesional con el historial completo de préstamos y operaciones
    de un laboratorio específico, organizando los datos en un formato claro y legible.

    Características del PDF:
        - Formato horizontal (A4 landscape) para mejor visualización de datos.
        - Diseño profesional con estilos personalizados.
        - Incluye todos los campos relevantes de cada registro.
        - Organiza reportes y materiales en filas combinadas.
        - Encabezado y pie de página estilizados.
        - Ordenamiento cronológico por fecha de finalización.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"""
            SELECT 
                ncontrol, hora_solicitud, fecha_solicitud, hora_final, fecha_final,
                name, lastname, teacher, casetero, topic, grupo, number_group,
                laboratory, tipo_vale, reporte, i_material
            FROM registro
            WHERE ({condition})
            ORDER BY fecha_final ASC
            """
    datos = obtenerDatosDB_Varios_Descarga(sql)

    columnas = [
        "ID", "Hora Solicitud", "Fecha Solicitud", "Hora Final", "Fecha Final",
        "Nombre", "Apellido", "Profesor", "Casetero", "Tema", "Grupo", "No. Grupo",
        "LAB", "Vale", 'Reporte', 'Materiales'
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
    content.append(Paragraph(f"Registros - {laboratorio}", styles['Title']))
    content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Procesamos los datos
    all_tables = []
    
    # Definir anchos de columnas proporcionales
    col_widths = [50, 40, 50, 40, 50, 60, 60, 60, 60, 50, 30, 30, 30, 50]
    
    # Cabecera de la tabla
    header_row = [Paragraph(col.upper(), style_header) for col in columnas[:-2]]  # Excluimos reporte y materiales
    all_tables.append(header_row)
    
    for fila in datos:
        main_data = []
        for item in fila[:-2]:  # Excluimos las columnas de reporte e i_material
            text = str(item)
            main_data.append(Paragraph(text, style_normal))
        all_tables.append(main_data)

        # Fila combinada de REPORTE y MATERIAL
        reporte_text = f"<b>REPORTE:</b><br/>{fila[-2]}"
        materiales = json.loads(fila[-1])
        material_items = [f"> {m[0]} - {m[1]}" for m in materiales if len(m) == 2]
        material_text = f"<b>MATERIAL:</b><br/>" + "<br/>".join(material_items)

        # Crear los dos párrafos
        reporte_paragraph = Paragraph(reporte_text, style_normal)
        material_paragraph = Paragraph(material_text, style_normal)

        # Fila de dos celdas con contenido, resto en blanco
        num_cols = len(col_widths)
        half_cols = num_cols // 2

        # Primera celda ocupa la mitad izquierda, segunda celda la derecha
        fila_extra = [reporte_paragraph] + [''] * (half_cols - 1) + [material_paragraph] + [''] * (num_cols - half_cols - 1)
        all_tables.append(fila_extra)

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
        if all_tables[i][1:] == [''] * (len(col_widths) - 1):  # Solo una celda con texto (caso antiguo)
            table_styles.append(('SPAN', (0, i), (-1, i)))
        elif all_tables[i].count('') == len(col_widths) - 2:  # Dos celdas con texto, el nuevo caso
            table_styles.append(('SPAN', (0, i), (half_cols - 1, i)))  # Span para reporte
            table_styles.append(('SPAN', (half_cols, i), (num_cols - 1, i)))  # Span para material

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