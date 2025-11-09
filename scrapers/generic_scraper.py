"""
Scraper genérico configurable para múltiples organizaciones del tercer sector
"""
from scrapers.base_scraper import BaseScraper
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)


class GenericScraper(BaseScraper):
    """
    Scraper genérico configurable mediante selectores CSS/XPath
    """

    def __init__(self, config: Dict):
        """
        Inicializa el scraper con configuración específica

        Args:
            config: Diccionario con configuración:
                - organization_name: Nombre de la organización
                - base_url: URL base
                - events_url: URL de la página de eventos
                - selectors: Selectores CSS para diferentes campos
                - pais: País de la organización
                - categoria_default: Categoría por defecto
        """
        super().__init__(
            organization_name=config['organization_name'],
            base_url=config['base_url']
        )
        self.events_url = config.get('events_url', self.base_url)
        self.selectors = config.get('selectors', {})
        self.pais = config.get('pais', 'España')
        self.categoria_default = config.get('categoria_default', 'Tercer sector')

    def scrape(self) -> List[Dict]:
        """Scrapea eventos usando la configuración proporcionada"""
        events = []
        try:
            soup = self.fetch_page(self.events_url)
            if not soup:
                return events

            # Buscar elementos de eventos
            container_selector = self.selectors.get('container', 'article')
            event_items = soup.select(container_selector)

            for item in event_items:
                try:
                    event = self.parse_event_item(item)
                    if event and self.validate_event(event):
                        normalized_event = self.normalize_event(event)
                        events.append(normalized_event)
                except Exception as e:
                    logger.error(f"Error parsing event item: {e}")
                    continue

            logger.info(f"Found {len(events)} events from {self.organization_name}")

        except Exception as e:
            logger.error(f"Error scraping {self.organization_name}: {e}")

        return events

    def parse_event_item(self, item) -> Dict:
        """Parsea un elemento de evento usando los selectores configurados"""
        event = {}

        # Título
        title_selector = self.selectors.get('title', 'h2, h3')
        title_elem = item.select_one(title_selector)
        if title_elem:
            event['nombre'] = title_elem.get_text(strip=True)

        # Fecha
        date_selector = self.selectors.get('date', 'time, .date')
        date_elem = item.select_one(date_selector)
        if date_elem:
            date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
            event['fecha'] = self.parse_date(date_text)

        # Enlace
        link_selector = self.selectors.get('link', 'a')
        link_elem = item.select_one(link_selector)
        if link_elem and link_elem.get('href'):
            href = link_elem['href']
            event['enlace'] = href if href.startswith('http') else f"{self.base_url}{href}"

        # Lugar
        location_selector = self.selectors.get('location', '.location, .lugar')
        location_elem = item.select_one(location_selector)
        if location_elem:
            location_text = location_elem.get_text(strip=True)
            if 'online' in location_text.lower():
                event['modalidad'] = 'Online'
                event['lugar'] = ''
            else:
                event['modalidad'] = 'Presencial'
                event['lugar'] = location_text

        event['entidad'] = self.organization_name
        event['pais'] = self.pais
        event['categoria'] = self.categoria_default

        return event

    def parse_date(self, date_text: str) -> str:
        """Parsea diferentes formatos de fecha"""
        try:
            # Formato ISO
            if re.match(r'\d{4}-\d{2}-\d{2}', date_text):
                return date_text[:10]

            # Formato DD/MM/YYYY o DD-MM-YYYY
            match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', date_text)
            if match:
                day, month, year = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # Formato YYYY/MM/DD
            match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', date_text)
            if match:
                year, month, day = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {e}")

        return ""


# Configuraciones predefinidas para organizaciones españolas
SPANISH_ORGANIZATIONS = [
    {
        'organization_name': 'Fundación La Caixa',
        'base_url': 'https://fundacionlacaixa.org',
        'events_url': 'https://fundacionlacaixa.org/es/agenda',
        'pais': 'España',
        'categoria_default': 'Cooperación internacional y desarrollo',
        'selectors': {
            'container': 'article.event, .event-card',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a',
            'location': '.location'
        }
    },
    {
        'organization_name': 'Entreculturas',
        'base_url': 'https://www.entreculturas.org',
        'events_url': 'https://www.entreculturas.org/es/agenda',
        'pais': 'España',
        'categoria_default': 'Cooperación internacional y desarrollo',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Fundación Telefónica',
        'base_url': 'https://www.fundaciontelefonica.com',
        'events_url': 'https://www.fundaciontelefonica.com/eventos',
        'pais': 'España',
        'categoria_default': 'Uso de IA en el tercer sector',
        'selectors': {
            'container': 'article, .event-card',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'CEAR',
        'base_url': 'https://www.cear.es',
        'events_url': 'https://www.cear.es/agenda',
        'pais': 'España',
        'categoria_default': 'Acompañamiento a migrantes',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Ayuda en Acción',
        'base_url': 'https://ayudaenaccion.org',
        'events_url': 'https://ayudaenaccion.org/actualidad/eventos',
        'pais': 'España',
        'categoria_default': 'Cooperación internacional y desarrollo',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    }
]
