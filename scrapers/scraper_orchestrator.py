"""
Orquestador de scrapers para coordinar la recolección de eventos
"""
from typing import List, Dict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.fundacion_once_scraper import FundacionOnceScraper
from scrapers.save_the_children_scraper import SaveTheChildrenScraper
from scrapers.generic_scraper import GenericScraper, SPANISH_ORGANIZATIONS
from scrapers.colombia_organizations import COLOMBIAN_ORGANIZATIONS

logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """
    Coordina la ejecución de múltiples scrapers en paralelo
    """

    def __init__(self):
        self.scrapers = []
        self.initialize_scrapers()

    def initialize_scrapers(self):
        """Inicializa todos los scrapers disponibles"""
        # Scrapers específicos
        self.scrapers.append(FundacionOnceScraper())
        self.scrapers.append(SaveTheChildrenScraper())

        # Scrapers genéricos para organizaciones españolas
        for org_config in SPANISH_ORGANIZATIONS:
            self.scrapers.append(GenericScraper(org_config))

        # Scrapers genéricos para organizaciones colombianas
        for org_config in COLOMBIAN_ORGANIZATIONS:
            self.scrapers.append(GenericScraper(org_config))

        logger.info(f"Initialized {len(self.scrapers)} scrapers")

    def run_all_scrapers(self, max_workers: int = 5) -> List[Dict]:
        """
        Ejecuta todos los scrapers en paralelo

        Args:
            max_workers: Número máximo de scrapers ejecutándose simultáneamente

        Returns:
            Lista consolidada de todos los eventos encontrados
        """
        all_events = []
        completed_scrapers = 0
        total_scrapers = len(self.scrapers)

        logger.info(f"Starting scraping process with {total_scrapers} scrapers")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todos los scrapers a ejecución
            future_to_scraper = {
                executor.submit(scraper.scrape): scraper
                for scraper in self.scrapers
            }

            # Procesar resultados a medida que se completan
            for future in as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    events = future.result()
                    all_events.extend(events)
                    completed_scrapers += 1
                    logger.info(
                        f"Completed {scraper.organization_name} "
                        f"({completed_scrapers}/{total_scrapers}): "
                        f"{len(events)} events found"
                    )
                except Exception as e:
                    logger.error(f"Error in {scraper.organization_name}: {e}")
                    completed_scrapers += 1

        logger.info(f"Scraping completed. Total events: {len(all_events)}")
        return all_events

    def run_single_scraper(self, organization_name: str) -> List[Dict]:
        """
        Ejecuta un scraper específico por nombre de organización

        Args:
            organization_name: Nombre de la organización

        Returns:
            Lista de eventos de esa organización
        """
        for scraper in self.scrapers:
            if scraper.organization_name == organization_name:
                logger.info(f"Running scraper for {organization_name}")
                return scraper.scrape()

        logger.warning(f"No scraper found for {organization_name}")
        return []

    def get_available_organizations(self) -> List[str]:
        """
        Obtiene lista de organizaciones disponibles

        Returns:
            Lista de nombres de organizaciones
        """
        return [scraper.organization_name for scraper in self.scrapers]
