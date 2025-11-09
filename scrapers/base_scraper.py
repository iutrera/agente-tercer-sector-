"""
Clase base para todos los scrapers del proyecto SIRIA
"""
import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Clase base para scrapers de eventos del tercer sector"""

    def __init__(self, organization_name: str, base_url: str):
        self.organization_name = organization_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Obtiene una página web con reintentos automáticos

        Args:
            url: URL a obtener

        Returns:
            BeautifulSoup object o None si falla
        """
        try:
            logger.info(f"Fetching {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            raise

    def generate_event_id(self, event_data: Dict) -> str:
        """
        Genera un ID único para un evento basado en enlace y fecha

        Args:
            event_data: Diccionario con datos del evento

        Returns:
            Hash único del evento
        """
        unique_string = f"{event_data.get('enlace', '')}{event_data.get('fecha', '')}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def normalize_event(self, event_data: Dict) -> Dict:
        """
        Normaliza un evento al formato estándar

        Args:
            event_data: Datos del evento a normalizar

        Returns:
            Evento normalizado con estructura estándar
        """
        normalized = {
            "id": self.generate_event_id(event_data),
            "nombre": event_data.get("nombre", ""),
            "entidad": event_data.get("entidad", self.organization_name),
            "fecha": event_data.get("fecha", ""),
            "hora": event_data.get("hora", ""),
            "modalidad": event_data.get("modalidad", ""),
            "lugar": event_data.get("lugar", ""),
            "enlace": event_data.get("enlace", ""),
            "pais": event_data.get("pais", "España"),
            "categoria": event_data.get("categoria", ""),
            "descripcion": event_data.get("descripcion", ""),
            "scraped_at": datetime.now().isoformat()
        }
        return normalized

    def scrape(self) -> List[Dict]:
        """
        Método abstracto que debe implementar cada scraper específico

        Returns:
            Lista de eventos scrapeados
        """
        raise NotImplementedError("Subclasses must implement scrape()")

    def validate_event(self, event: Dict) -> bool:
        """
        Valida que un evento tenga los campos mínimos requeridos

        Args:
            event: Evento a validar

        Returns:
            True si el evento es válido, False en caso contrario
        """
        required_fields = ["nombre", "entidad", "fecha", "enlace"]
        return all(event.get(field) for field in required_fields)
