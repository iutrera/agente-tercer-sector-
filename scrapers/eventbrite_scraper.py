"""
Scraper para eventos de Eventbrite relacionados con el tercer sector
"""
from scrapers.base_scraper import BaseScraper
from typing import List, Dict
import logging
import requests

logger = logging.getLogger(__name__)


class EventbriteScraper(BaseScraper):
    """
    Scraper para Eventbrite usando su API
    Requiere API key de Eventbrite
    """

    def __init__(self, api_key: str = None):
        super().__init__(
            organization_name="Eventbrite",
            base_url="https://www.eventbriteapi.com/v3"
        )
        self.api_key = api_key
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })

        # Palabras clave para buscar eventos del tercer sector
        self.keywords = [
            'tercer sector',
            'inclusión laboral',
            'formación profesional',
            'cooperación internacional',
            'migrantes',
            'refugiados',
            'ong',
            'fundación',
            'asociación',
            'voluntariado',
            'derechos humanos',
            'infancia',
            'juventud',
            'mujeres'
        ]

    def scrape(self) -> List[Dict]:
        """
        Scrapea eventos de Eventbrite

        Returns:
            Lista de eventos encontrados
        """
        if not self.api_key:
            logger.warning("No Eventbrite API key provided, using web scraping fallback")
            return self.scrape_web()

        all_events = []

        # Buscar eventos para España y Colombia
        for country in ['ES', 'CO']:
            for keyword in self.keywords[:5]:  # Limitar búsquedas para no exceder rate limits
                try:
                    events = self.search_events(keyword, country)
                    all_events.extend(events)
                except Exception as e:
                    logger.error(f"Error searching '{keyword}' in {country}: {e}")

        logger.info(f"Found {len(all_events)} events from Eventbrite")
        return all_events

    def search_events(self, keyword: str, country_code: str) -> List[Dict]:
        """
        Busca eventos en Eventbrite API

        Args:
            keyword: Palabra clave a buscar
            country_code: Código de país (ES, CO)

        Returns:
            Lista de eventos
        """
        events = []

        try:
            url = f"{self.base_url}/events/search/"
            params = {
                'q': keyword,
                'location.address': country_code,
                'expand': 'venue',
                'sort_by': 'date'
            }

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for event_data in data.get('events', []):
                event = self.parse_api_event(event_data, country_code)
                if event and self.validate_event(event):
                    events.append(self.normalize_event(event))

        except Exception as e:
            logger.error(f"Error in API search: {e}")

        return events

    def parse_api_event(self, event_data: Dict, country_code: str) -> Dict:
        """
        Parsea un evento de la API de Eventbrite

        Args:
            event_data: Datos del evento desde la API
            country_code: Código del país

        Returns:
            Evento parseado
        """
        event = {}

        event['nombre'] = event_data.get('name', {}).get('text', '')
        event['descripcion'] = event_data.get('description', {}).get('text', '')
        event['enlace'] = event_data.get('url', '')

        # Fecha y hora
        start = event_data.get('start', {})
        event['fecha'] = start.get('local', '').split('T')[0] if start.get('local') else ''
        event['hora'] = start.get('local', '').split('T')[1][:5] if start.get('local') and 'T' in start.get('local', '') else ''

        # Modalidad y lugar
        if event_data.get('online_event'):
            event['modalidad'] = 'Online'
            event['lugar'] = ''
        else:
            event['modalidad'] = 'Presencial'
            venue = event_data.get('venue', {})
            address = venue.get('address', {})
            event['lugar'] = f"{address.get('city', '')}, {address.get('region', '')}"

        event['entidad'] = event_data.get('organizer', {}).get('name', 'Eventbrite')
        event['pais'] = 'España' if country_code == 'ES' else 'Colombia'
        event['categoria'] = self.categorize_event(event['nombre'], event.get('descripcion', ''))

        return event

    def scrape_web(self) -> List[Dict]:
        """
        Fallback: scraping web cuando no hay API key

        Returns:
            Lista de eventos scrapeados
        """
        events = []
        # Implementar scraping web como fallback
        # Por ahora retornar lista vacía
        logger.info("Web scraping fallback not yet implemented")
        return events

    def categorize_event(self, title: str, description: str) -> str:
        """
        Categoriza un evento basándose en título y descripción

        Args:
            title: Título del evento
            description: Descripción del evento

        Returns:
            Categoría del evento
        """
        text = f"{title} {description}".lower()

        if any(word in text for word in ['empleo', 'laboral', 'trabajo', 'inserción']):
            return 'Inclusión laboral'
        elif any(word in text for word in ['formación', 'curso', 'capacitación']):
            return 'Formación profesional'
        elif any(word in text for word in ['migrant', 'refugiad', 'acogida']):
            return 'Acompañamiento a migrantes'
        elif any(word in text for word in ['cooperación', 'desarrollo', 'internacional']):
            return 'Cooperación internacional y desarrollo'
        elif any(word in text for word in ['niñ', 'infancia', 'joven', 'mujer']):
            return 'Derechos de infancia, juventud y mujeres'
        elif any(word in text for word in ['ia', 'inteligencia artificial', 'digital', 'tecnología']):
            return 'Uso de IA en el tercer sector'
        else:
            return 'Tercer sector'
