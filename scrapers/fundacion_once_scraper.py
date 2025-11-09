"""
Scraper para Fundación ONCE
https://www.fundaciononce.es
"""
from scrapers.base_scraper import BaseScraper
from typing import List, Dict
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class FundacionOnceScraper(BaseScraper):
    """Scraper específico para eventos de Fundación ONCE"""

    def __init__(self):
        super().__init__(
            organization_name="Fundación ONCE",
            base_url="https://www.fundaciononce.es"
        )
        self.events_url = f"{self.base_url}/es/agenda"

    def scrape(self) -> List[Dict]:
        """
        Scrapea eventos de Fundación ONCE

        Returns:
            Lista de eventos encontrados
        """
        events = []
        try:
            soup = self.fetch_page(self.events_url)
            if not soup:
                return events

            # Buscar eventos en la agenda
            # NOTA: Esta es una implementación genérica
            # Ajustar selectores según la estructura real del sitio
            event_items = soup.find_all('article', class_=re.compile('event|evento|agenda'))

            for item in event_items:
                try:
                    event = self.parse_event_item(item)
                    if event and self.validate_event(event):
                        normalized_event = self.normalize_event(event)
                        events.append(normalized_event)
                except Exception as e:
                    logger.error(f"Error parsing event item: {e}")
                    continue

            logger.info(f"Found {len(events)} events from Fundación ONCE")

        except Exception as e:
            logger.error(f"Error scraping Fundación ONCE: {e}")

        return events

    def parse_event_item(self, item) -> Dict:
        """
        Parsea un elemento de evento individual

        Args:
            item: BeautifulSoup element del evento

        Returns:
            Diccionario con datos del evento
        """
        event = {}

        # Título
        title_elem = item.find(['h2', 'h3', 'h4'], class_=re.compile('title|titulo|name'))
        if title_elem:
            event['nombre'] = title_elem.get_text(strip=True)

        # Fecha
        date_elem = item.find(['time', 'span', 'div'], class_=re.compile('date|fecha'))
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            event['fecha'] = self.parse_date(date_text)

        # Enlace
        link_elem = item.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            event['enlace'] = href if href.startswith('http') else f"{self.base_url}{href}"

        # Lugar/Modalidad
        location_elem = item.find(['span', 'div'], class_=re.compile('location|lugar|place'))
        if location_elem:
            location_text = location_elem.get_text(strip=True)
            if 'online' in location_text.lower() or 'virtual' in location_text.lower():
                event['modalidad'] = 'Online'
                event['lugar'] = ''
            else:
                event['modalidad'] = 'Presencial'
                event['lugar'] = location_text

        # Categoría (basada en contenido)
        event['categoria'] = self.infer_category(event.get('nombre', ''))

        event['entidad'] = self.organization_name
        event['pais'] = 'España'

        return event

    def parse_date(self, date_text: str) -> str:
        """
        Intenta parsear diferentes formatos de fecha

        Args:
            date_text: Texto con la fecha

        Returns:
            Fecha en formato YYYY-MM-DD
        """
        # Implementar parseo de fechas en español
        # Por ahora, devolver fecha actual como placeholder
        try:
            # Buscar patrón DD/MM/YYYY o DD-MM-YYYY
            match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', date_text)
            if match:
                day, month, year = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # Buscar patrón YYYY-MM-DD
            match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_text)
            if match:
                return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"

        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {e}")

        return ""

    def infer_category(self, text: str) -> str:
        """
        Infiere la categoría del evento basándose en palabras clave

        Args:
            text: Texto del título o descripción

        Returns:
            Categoría inferida
        """
        text_lower = text.lower()

        if any(word in text_lower for word in ['empleo', 'laboral', 'trabajo', 'inserción']):
            return 'Inclusión laboral'
        elif any(word in text_lower for word in ['formación', 'curso', 'taller', 'capacitación']):
            return 'Formación profesional'
        elif any(word in text_lower for word in ['discapacidad', 'accesibilidad', 'inclusión']):
            return 'Inclusión laboral'
        elif any(word in text_lower for word in ['cooperación', 'desarrollo', 'internacional']):
            return 'Cooperación internacional y desarrollo'
        else:
            return 'Inclusión laboral'  # Default para Fundación ONCE
