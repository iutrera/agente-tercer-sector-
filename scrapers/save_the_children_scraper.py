"""
Scraper para Save the Children España
https://www.savethechildren.es
"""
from scrapers.base_scraper import BaseScraper
from typing import List, Dict
import logging
import re

logger = logging.getLogger(__name__)


class SaveTheChildrenScraper(BaseScraper):
    """Scraper específico para eventos de Save the Children España"""

    def __init__(self):
        super().__init__(
            organization_name="Save the Children España",
            base_url="https://www.savethechildren.es"
        )
        self.events_url = f"{self.base_url}/actualidad/eventos"

    def scrape(self) -> List[Dict]:
        """
        Scrapea eventos de Save the Children

        Returns:
            Lista de eventos encontrados
        """
        events = []
        try:
            soup = self.fetch_page(self.events_url)
            if not soup:
                return events

            # Buscar eventos
            event_items = soup.find_all(['article', 'div'], class_=re.compile('event|evento|card'))

            for item in event_items:
                try:
                    event = self.parse_event_item(item)
                    if event and self.validate_event(event):
                        normalized_event = self.normalize_event(event)
                        events.append(normalized_event)
                except Exception as e:
                    logger.error(f"Error parsing event item: {e}")
                    continue

            logger.info(f"Found {len(events)} events from Save the Children")

        except Exception as e:
            logger.error(f"Error scraping Save the Children: {e}")

        return events

    def parse_event_item(self, item) -> Dict:
        """Parsea un elemento de evento individual"""
        event = {}

        # Título
        title_elem = item.find(['h2', 'h3', 'h4', 'a'])
        if title_elem:
            event['nombre'] = title_elem.get_text(strip=True)

        # Fecha
        date_elem = item.find(['time', 'span', 'div'], class_=re.compile('date|fecha|time'))
        if date_elem:
            date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
            event['fecha'] = self.parse_date(date_text)

        # Enlace
        link_elem = item.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            event['enlace'] = href if href.startswith('http') else f"{self.base_url}{href}"

        # Categoría
        event['categoria'] = 'Derechos de infancia, juventud y mujeres'
        event['entidad'] = self.organization_name
        event['pais'] = 'España'
        event['modalidad'] = 'Presencial'

        return event

    def parse_date(self, date_text: str) -> str:
        """Parsea fecha al formato estándar"""
        try:
            # Si ya está en formato ISO
            if re.match(r'\d{4}-\d{2}-\d{2}', date_text):
                return date_text[:10]

            # Buscar patrón DD/MM/YYYY
            match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', date_text)
            if match:
                day, month, year = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {e}")

        return ""
