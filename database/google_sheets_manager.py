"""
Gestor de Google Sheets para almacenar eventos
"""
import os
from typing import List, Dict, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Google Sheets se importa condicionalmente
try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google API libraries not available. Install with: pip install google-api-python-client google-auth")


class GoogleSheetsManager:
    """
    Gestiona el almacenamiento y actualización de eventos en Google Sheets
    """

    # Columnas del sheet según especificación
    COLUMNS = [
        'ID',
        'Nombre del evento',
        'Entidad organizadora',
        'Fecha',
        'Hora',
        'Modalidad',
        'Lugar',
        'Enlace de inscripción',
        'País',
        'Categoría temática',
        'Descripción',
        'Última actualización'
    ]

    def __init__(self, credentials_file: Optional[str] = None, spreadsheet_id: Optional[str] = None):
        """
        Inicializa el gestor de Google Sheets

        Args:
            credentials_file: Ruta al archivo de credenciales JSON
            spreadsheet_id: ID de la hoja de cálculo
        """
        if not GOOGLE_AVAILABLE:
            logger.error("Google API libraries not installed")
            self.service = None
            return

        self.credentials_file = credentials_file or os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        self.service = None

        if self.credentials_file and os.path.exists(self.credentials_file):
            self.authenticate()
        else:
            logger.warning("Google Sheets credentials not configured")

    def authenticate(self):
        """Autentica con Google Sheets API"""
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=SCOPES
            )

            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Successfully authenticated with Google Sheets API")

        except Exception as e:
            logger.error(f"Error authenticating with Google Sheets: {e}")
            self.service = None

    def create_sheet(self, sheet_name: str = "Eventos Tercer Sector") -> bool:
        """
        Crea una nueva hoja con encabezados

        Args:
            sheet_name: Nombre de la hoja

        Returns:
            True si se creó exitosamente
        """
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets not configured")
            return False

        try:
            # Crear hoja
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=request_body
            ).execute()

            # Añadir encabezados
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption='RAW',
                body={'values': [self.COLUMNS]}
            ).execute()

            logger.info(f"Sheet '{sheet_name}' created successfully")
            return True

        except HttpError as e:
            if 'already exists' in str(e):
                logger.info(f"Sheet '{sheet_name}' already exists")
                return True
            logger.error(f"Error creating sheet: {e}")
            return False

    def event_to_row(self, event: Dict) -> List:
        """
        Convierte un evento a una fila para Google Sheets

        Args:
            event: Diccionario con datos del evento

        Returns:
            Lista con valores para cada columna
        """
        return [
            event.get('id', ''),
            event.get('nombre', ''),
            event.get('entidad', ''),
            event.get('fecha', ''),
            event.get('hora', ''),
            event.get('modalidad', ''),
            event.get('lugar', ''),
            event.get('enlace', ''),
            event.get('pais', ''),
            event.get('categoria', ''),
            event.get('descripcion', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]

    def append_events(self, events: List[Dict], sheet_name: str = "Eventos Tercer Sector") -> bool:
        """
        Añade eventos a la hoja

        Args:
            events: Lista de eventos
            sheet_name: Nombre de la hoja

        Returns:
            True si se añadieron exitosamente
        """
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets not configured")
            return False

        if not events:
            logger.info("No events to append")
            return True

        try:
            # Convertir eventos a filas
            rows = [self.event_to_row(event) for event in events]

            # Añadir filas
            body = {'values': rows}

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A2",
                valueInputOption='RAW',
                body=body
            ).execute()

            logger.info(f"Added {len(events)} events to sheet '{sheet_name}'")
            return True

        except Exception as e:
            logger.error(f"Error appending events: {e}")
            return False

    def get_all_events(self, sheet_name: str = "Eventos Tercer Sector") -> List[Dict]:
        """
        Obtiene todos los eventos de la hoja

        Args:
            sheet_name: Nombre de la hoja

        Returns:
            Lista de eventos
        """
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets not configured")
            return []

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A2:L"
            ).execute()

            rows = result.get('values', [])

            events = []
            for row in rows:
                # Asegurar que la fila tenga todas las columnas
                while len(row) < len(self.COLUMNS):
                    row.append('')

                event = {
                    'id': row[0],
                    'nombre': row[1],
                    'entidad': row[2],
                    'fecha': row[3],
                    'hora': row[4],
                    'modalidad': row[5],
                    'lugar': row[6],
                    'enlace': row[7],
                    'pais': row[8],
                    'categoria': row[9],
                    'descripcion': row[10],
                    'ultima_actualizacion': row[11]
                }
                events.append(event)

            logger.info(f"Retrieved {len(events)} events from sheet")
            return events

        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []

    def update_event(self, event_id: str, updated_data: Dict, sheet_name: str = "Eventos Tercer Sector") -> bool:
        """
        Actualiza un evento existente

        Args:
            event_id: ID del evento
            updated_data: Datos actualizados
            sheet_name: Nombre de la hoja

        Returns:
            True si se actualizó exitosamente
        """
        if not self.service or not self.spreadsheet_id:
            return False

        try:
            # Obtener todos los eventos
            events = self.get_all_events(sheet_name)

            # Buscar el índice del evento
            for i, event in enumerate(events):
                if event['id'] == event_id:
                    # Actualizar datos
                    event.update(updated_data)
                    event['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Actualizar fila (i+2 porque hay encabezado y las filas empiezan en 1)
                    row_number = i + 2
                    row_data = self.event_to_row(event)

                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.spreadsheet_id,
                        range=f"{sheet_name}!A{row_number}:L{row_number}",
                        valueInputOption='RAW',
                        body={'values': [row_data]}
                    ).execute()

                    logger.info(f"Updated event {event_id}")
                    return True

            logger.warning(f"Event {event_id} not found")
            return False

        except Exception as e:
            logger.error(f"Error updating event: {e}")
            return False

    def clear_sheet(self, sheet_name: str = "Eventos Tercer Sector") -> bool:
        """
        Limpia todos los datos de la hoja (mantiene encabezados)

        Args:
            sheet_name: Nombre de la hoja

        Returns:
            True si se limpió exitosamente
        """
        if not self.service or not self.spreadsheet_id:
            return False

        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A2:L"
            ).execute()

            logger.info(f"Cleared sheet '{sheet_name}'")
            return True

        except Exception as e:
            logger.error(f"Error clearing sheet: {e}")
            return False
