"""
Sistema de actualización semanal de eventos
"""
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import base64

# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_orchestrator import ScraperOrchestrator
from classifiers.event_classifier import EventClassifier
from utils.deduplication import EventDeduplicator
from utils.excel_generator import ExcelGenerator
from database.google_sheets_manager import GoogleSheetsManager

logger = logging.getLogger(__name__)


class WeeklyUpdater:
    """
    Coordina el proceso semanal de actualización de eventos
    """

    def __init__(self):
        """Inicializa todos los componentes del sistema"""
        self.scraper_orchestrator = ScraperOrchestrator()
        self.classifier = EventClassifier()
        self.deduplicator = EventDeduplicator()
        self.excel_generator = ExcelGenerator()
        self.sheets_manager = GoogleSheetsManager()

        logger.info("WeeklyUpdater initialized")

    def run_full_update(self) -> Dict:
        """
        Ejecuta el proceso completo de actualización

        Returns:
            Diccionario con resultados del proceso
        """
        logger.info("=" * 80)
        logger.info("STARTING WEEKLY UPDATE PROCESS")
        logger.info("=" * 80)

        results = {
            'start_time': datetime.now().isoformat(),
            'events_scraped': 0,
            'events_deduplicated': 0,
            'events_classified': 0,
            'events_stored': 0,
            'excel_file': None,
            'errors': []
        }

        try:
            # 1. Scraping de eventos
            logger.info("STEP 1: Scraping events from all sources")
            all_events = self.scraper_orchestrator.run_all_scrapers()
            results['events_scraped'] = len(all_events)
            logger.info(f"Scraped {len(all_events)} events")

            if not all_events:
                logger.warning("No events scraped, aborting update")
                return results

            # 2. Clasificación de eventos
            logger.info("STEP 2: Classifying events")
            classified_events = self.classifier.classify_batch(all_events)
            results['events_classified'] = len(classified_events)
            logger.info(f"Classified {len(classified_events)} events")

            # 3. Deduplicación
            logger.info("STEP 3: Deduplicating events")
            unique_events = self.deduplicator.deduplicate(classified_events)
            results['events_deduplicated'] = len(unique_events)
            logger.info(f"After deduplication: {len(unique_events)} unique events")

            # 4. Filtrar eventos por rango de fechas (próximos 12 meses)
            logger.info("STEP 4: Filtering events by date range")
            filtered_events = self.filter_events_by_date(unique_events)
            logger.info(f"After date filtering: {len(filtered_events)} events")

            # 5. Almacenar en Google Sheets
            logger.info("STEP 5: Storing events in Google Sheets")
            if self.sheets_manager.service:
                # Limpiar hoja anterior
                self.sheets_manager.clear_sheet()
                # Añadir nuevos eventos
                self.sheets_manager.append_events(filtered_events)
                results['events_stored'] = len(filtered_events)
                logger.info(f"Stored {len(filtered_events)} events in Google Sheets")
            else:
                logger.warning("Google Sheets not configured, skipping storage")

            # 6. Generar Excel
            logger.info("STEP 6: Generating Excel file")
            excel_file = self.excel_generator.generate_excel(filtered_events)
            results['excel_file'] = excel_file
            logger.info(f"Generated Excel file: {excel_file}")

            # 7. Generar reporte resumen
            logger.info("STEP 7: Generating summary report")
            summary_file = self.excel_generator.generate_summary_report(filtered_events)
            results['summary_file'] = summary_file
            logger.info(f"Generated summary report: {summary_file}")

            results['end_time'] = datetime.now().isoformat()
            results['status'] = 'success'

            logger.info("=" * 80)
            logger.info("WEEKLY UPDATE COMPLETED SUCCESSFULLY")
            logger.info(f"Total events: {len(filtered_events)}")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Error in weekly update: {e}", exc_info=True)
            results['errors'].append(str(e))
            results['status'] = 'failed'

        return results

    def filter_events_by_date(self, events: List[Dict], months_ahead: int = 12) -> List[Dict]:
        """
        Filtra eventos que ocurren en los próximos N meses

        Args:
            events: Lista de eventos
            months_ahead: Número de meses hacia adelante

        Returns:
            Lista de eventos filtrados
        """
        today = datetime.now().date()
        end_date = today + timedelta(days=30 * months_ahead)

        filtered = []
        for event in events:
            try:
                event_date_str = event.get('fecha', '')
                if not event_date_str:
                    continue

                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()

                if today <= event_date <= end_date:
                    filtered.append(event)

            except Exception as e:
                logger.error(f"Error parsing date for event {event.get('nombre', 'unknown')}: {e}")
                continue

        return filtered

    def send_weekly_email(self, results: Dict, recipient: str = "jcsiria@basecamp.world"):
        """
        Envía email semanal con resultados

        Args:
            results: Resultados del proceso de actualización
            recipient: Email del destinatario
        """
        import requests

        # Preparar cuerpo del email
        body = f"""
        <h2>Agenda Semanal de Eventos del Tercer Sector</h2>

        <p>Resumen de la actualización semanal:</p>

        <ul>
            <li><strong>Eventos scrapeados:</strong> {results.get('events_scraped', 0)}</li>
            <li><strong>Eventos únicos:</strong> {results.get('events_deduplicated', 0)}</li>
            <li><strong>Eventos clasificados:</strong> {results.get('events_classified', 0)}</li>
            <li><strong>Eventos almacenados:</strong> {results.get('events_stored', 0)}</li>
        </ul>

        <p>Archivo Excel adjunto con todos los eventos encontrados.</p>

        <p><em>Generado automáticamente por SIRIA - {datetime.now().strftime('%Y-%m-%d %H:%M')}</em></p>
        """

        # Leer archivo Excel y convertir a base64
        excel_file = results.get('excel_file')
        if excel_file and os.path.exists(excel_file):
            with open(excel_file, 'rb') as f:
                excel_data = f.read()
                excel_base64 = base64.b64encode(excel_data).decode('utf-8')

            filename = os.path.basename(excel_file)
        else:
            logger.error("Excel file not found, cannot send email")
            return

        # Llamar al endpoint de send_email
        try:
            api_url = os.getenv('API_URL', 'http://localhost:8000')
            token = os.getenv('SECRET_TOKEN', '')

            response = requests.post(
                f"{api_url}/send_email",
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                },
                json={
                    'to': recipient,
                    'subject': f'Agenda Semanal de Eventos del Tercer Sector - {datetime.now().strftime("%Y-%m-%d")}',
                    'body': body,
                    'content_type': 'html',
                    'attachment_base64': excel_base64,
                    'filename': filename
                },
                timeout=60
            )

            if response.status_code == 200:
                logger.info(f"Email sent successfully to {recipient}")
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"Error sending email: {e}")


def main():
    """Función principal para ejecutar actualización"""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('siria_weekly_update.log'),
            logging.StreamHandler()
        ]
    )

    updater = WeeklyUpdater()
    results = updater.run_full_update()

    # Enviar email con resultados
    if results.get('status') == 'success':
        updater.send_weekly_email(results)

    return results


if __name__ == '__main__':
    main()
