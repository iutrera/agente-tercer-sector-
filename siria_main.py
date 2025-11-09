"""
SIRIA - Sistema de Recopilación e Identificación de Recursos e Información Actualizada
Punto de entrada principal del sistema
"""
import os
import sys
import argparse
import logging
from datetime import datetime

from scrapers.scraper_orchestrator import ScraperOrchestrator
from classifiers.event_classifier import EventClassifier
from utils.deduplication import EventDeduplicator
from utils.excel_generator import ExcelGenerator
from database.google_sheets_manager import GoogleSheetsManager
from schedulers.weekly_updater import WeeklyUpdater

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'siria_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='SIRIA - Sistema de Recopilación de Eventos del Tercer Sector'
    )

    parser.add_argument(
        'command',
        choices=['scrape', 'update', 'schedule', 'test'],
        help='Comando a ejecutar'
    )

    parser.add_argument(
        '--org',
        type=str,
        help='Nombre de organización específica para scraping'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='Directorio de salida para archivos Excel'
    )

    parser.add_argument(
        '--no-email',
        action='store_true',
        help='No enviar email con resultados'
    )

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info(f"SIRIA - Starting command: {args.command}")
    logger.info("=" * 80)

    if args.command == 'scrape':
        # Solo hacer scraping sin clasificar ni almacenar
        orchestrator = ScraperOrchestrator()

        if args.org:
            events = orchestrator.run_single_scraper(args.org)
            logger.info(f"Scraped {len(events)} events from {args.org}")
        else:
            events = orchestrator.run_all_scrapers()
            logger.info(f"Scraped {len(events)} total events")

        # Generar Excel simple
        excel_gen = ExcelGenerator(args.output)
        excel_file = excel_gen.generate_excel(events)
        logger.info(f"Excel file generated: {excel_file}")

    elif args.command == 'update':
        # Ejecutar actualización completa
        updater = WeeklyUpdater()
        results = updater.run_full_update()

        if results.get('status') == 'success':
            logger.info("Update completed successfully")

            # Enviar email si no está deshabilitado
            if not args.no_email:
                updater.send_weekly_email(results)
        else:
            logger.error("Update failed")
            logger.error(f"Errors: {results.get('errors', [])}")
            sys.exit(1)

    elif args.command == 'schedule':
        # Iniciar scheduler para ejecución semanal
        from schedulers.scheduler import main as scheduler_main
        scheduler_main()

    elif args.command == 'test':
        # Modo de prueba - scrapea solo algunas organizaciones
        logger.info("Running in TEST mode")

        orchestrator = ScraperOrchestrator()
        classifier = EventClassifier()
        deduplicator = EventDeduplicator()
        excel_gen = ExcelGenerator(args.output)

        # Listar organizaciones disponibles
        orgs = orchestrator.get_available_organizations()
        logger.info(f"Available organizations: {len(orgs)}")
        for org in orgs[:5]:
            logger.info(f"  - {org}")

        # Scrapear primeras 3 organizaciones
        test_events = []
        for org in orgs[:3]:
            events = orchestrator.run_single_scraper(org)
            test_events.extend(events)
            logger.info(f"Scraped {len(events)} events from {org}")

        # Clasificar
        classified = classifier.classify_batch(test_events)
        logger.info(f"Classified {len(classified)} events")

        # Deduplicar
        unique = deduplicator.deduplicate(classified)
        logger.info(f"After deduplication: {len(unique)} unique events")

        # Generar Excel
        excel_file = excel_gen.generate_excel(unique, 'test_output.xlsx')
        logger.info(f"Test Excel generated: {excel_file}")

    logger.info("=" * 80)
    logger.info("SIRIA - Command completed")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
