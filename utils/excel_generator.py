"""
Generador de archivos Excel para exportar eventos
"""
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class ExcelGenerator:
    """
    Genera archivos Excel con el formato especificado para eventos
    """

    # Columnas según especificación del objetivo general
    COLUMN_MAPPING = {
        'nombre': 'Nombre del evento',
        'entidad': 'Entidad organizadora',
        'fecha': 'Fecha',
        'hora': 'Hora',
        'modalidad': 'Modalidad (Presencial / Online)',
        'lugar': 'Lugar',
        'enlace': 'Enlace de inscripción',
        'pais': 'País (España / Colombia)',
        'categoria': 'Categoría temática'
    }

    def __init__(self, output_dir: str = './output'):
        """
        Inicializa el generador de Excel

        Args:
            output_dir: Directorio donde guardar los archivos
        """
        self.output_dir = output_dir

        # Crear directorio si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

    def events_to_dataframe(self, events: List[Dict]) -> pd.DataFrame:
        """
        Convierte lista de eventos a DataFrame de pandas

        Args:
            events: Lista de eventos

        Returns:
            DataFrame con eventos
        """
        if not events:
            # Retornar DataFrame vacío con columnas
            return pd.DataFrame(columns=list(self.COLUMN_MAPPING.values()))

        # Preparar datos
        data = []
        for event in events:
            row = {
                self.COLUMN_MAPPING['nombre']: event.get('nombre', ''),
                self.COLUMN_MAPPING['entidad']: event.get('entidad', ''),
                self.COLUMN_MAPPING['fecha']: event.get('fecha', ''),
                self.COLUMN_MAPPING['hora']: event.get('hora', ''),
                self.COLUMN_MAPPING['modalidad']: event.get('modalidad', ''),
                self.COLUMN_MAPPING['lugar']: event.get('lugar', ''),
                self.COLUMN_MAPPING['enlace']: event.get('enlace', ''),
                self.COLUMN_MAPPING['pais']: event.get('pais', ''),
                self.COLUMN_MAPPING['categoria']: event.get('categoria', '')
            }
            data.append(row)

        df = pd.DataFrame(data)

        # Ordenar por fecha
        df = df.sort_values(by='Fecha', ascending=True)

        return df

    def generate_excel(self, events: List[Dict], filename: str = None) -> str:
        """
        Genera archivo Excel con eventos

        Args:
            events: Lista de eventos
            filename: Nombre del archivo (opcional)

        Returns:
            Ruta del archivo generado
        """
        # Generar nombre de archivo si no se proporciona
        if not filename:
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"agenda_eventos_tercer_sector_{date_str}.xlsx"

        filepath = os.path.join(self.output_dir, filename)

        # Convertir eventos a DataFrame
        df = self.events_to_dataframe(events)

        # Crear archivo Excel con formato
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Eventos', index=False)

            # Obtener workbook y worksheet para dar formato
            workbook = writer.book
            worksheet = writer.sheets['Eventos']

            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })

            link_format = workbook.add_format({
                'font_color': 'blue',
                'underline': True
            })

            cell_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'top',
                'text_wrap': True
            })

            # Aplicar formato a encabezados
            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)

            # Ajustar anchos de columna
            column_widths = {
                'Nombre del evento': 35,
                'Entidad organizadora': 25,
                'Fecha': 12,
                'Hora': 10,
                'Modalidad (Presencial / Online)': 20,
                'Lugar': 20,
                'Enlace de inscripción': 40,
                'País (España / Colombia)': 15,
                'Categoría temática': 30
            }

            for col_num, column in enumerate(df.columns):
                width = column_widths.get(column, 15)
                worksheet.set_column(col_num, col_num, width)

            # Aplicar formato de enlace a la columna de enlaces
            link_col_index = list(df.columns).index('Enlace de inscripción')
            for row_num in range(1, len(df) + 1):
                worksheet.write_url(
                    row_num, link_col_index,
                    df.iloc[row_num - 1]['Enlace de inscripción'],
                    link_format,
                    df.iloc[row_num - 1]['Enlace de inscripción']
                )

            # Congelar fila de encabezados
            worksheet.freeze_panes(1, 0)

            # Añadir autofiltro
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

        logger.info(f"Generated Excel file: {filepath} with {len(events)} events")
        return filepath

    def generate_excel_by_category(self, events: List[Dict], filename: str = None) -> str:
        """
        Genera Excel con múltiples hojas, una por categoría

        Args:
            events: Lista de eventos
            filename: Nombre del archivo

        Returns:
            Ruta del archivo generado
        """
        if not filename:
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"agenda_eventos_por_categoria_{date_str}.xlsx"

        filepath = os.path.join(self.output_dir, filename)

        # Agrupar eventos por categoría
        events_by_category = {}
        for event in events:
            category = event.get('categoria', 'Sin categoría')
            if category not in events_by_category:
                events_by_category[category] = []
            events_by_category[category].append(event)

        # Crear Excel con múltiples hojas
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            for category, cat_events in events_by_category.items():
                # Sanitizar nombre de hoja (Excel tiene límite de 31 caracteres)
                sheet_name = category[:31]

                df = self.events_to_dataframe(cat_events)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Formato básico
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]

                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#4472C4',
                    'font_color': 'white',
                    'border': 1
                })

                for col_num, column in enumerate(df.columns):
                    worksheet.write(0, col_num, column, header_format)
                    worksheet.set_column(col_num, col_num, 15)

        logger.info(f"Generated categorized Excel file: {filepath}")
        return filepath

    def generate_summary_report(self, events: List[Dict], filename: str = None) -> str:
        """
        Genera reporte resumen con estadísticas

        Args:
            events: Lista de eventos
            filename: Nombre del archivo

        Returns:
            Ruta del archivo generado
        """
        if not filename:
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"resumen_eventos_{date_str}.xlsx"

        filepath = os.path.join(self.output_dir, filename)

        # Crear DataFrames para diferentes análisis
        df_events = self.events_to_dataframe(events)

        # Estadísticas por categoría
        category_stats = df_events['Categoría temática'].value_counts().reset_index()
        category_stats.columns = ['Categoría', 'Cantidad de eventos']

        # Estadísticas por país
        country_stats = df_events['País (España / Colombia)'].value_counts().reset_index()
        country_stats.columns = ['País', 'Cantidad de eventos']

        # Estadísticas por modalidad
        modality_stats = df_events['Modalidad (Presencial / Online)'].value_counts().reset_index()
        modality_stats.columns = ['Modalidad', 'Cantidad de eventos']

        # Guardar en Excel con múltiples hojas
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            # Hoja de todos los eventos
            df_events.to_excel(writer, sheet_name='Todos los eventos', index=False)

            # Hojas de estadísticas
            category_stats.to_excel(writer, sheet_name='Por categoría', index=False)
            country_stats.to_excel(writer, sheet_name='Por país', index=False)
            modality_stats.to_excel(writer, sheet_name='Por modalidad', index=False)

            # Formato
            workbook = writer.book
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column(0, 10, 20)

        logger.info(f"Generated summary report: {filepath}")
        return filepath
