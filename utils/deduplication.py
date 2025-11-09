"""
Sistema de deduplicación de eventos
"""
import hashlib
from typing import List, Dict, Set
import logging
from datetime import datetime
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class EventDeduplicator:
    """
    Sistema para detectar y eliminar eventos duplicados
    """

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Inicializa el deduplicador

        Args:
            similarity_threshold: Umbral de similitud (0-1) para considerar eventos como duplicados
        """
        self.similarity_threshold = similarity_threshold
        self.seen_ids: Set[str] = set()

    def generate_event_id(self, event: Dict) -> str:
        """
        Genera un ID único para un evento

        Args:
            event: Evento

        Returns:
            Hash único del evento
        """
        # Usar enlace + fecha como identificador principal
        unique_string = f"{event.get('enlace', '')}{event.get('fecha', '')}"

        # Si no hay enlace, usar nombre + entidad + fecha
        if not event.get('enlace'):
            unique_string = f"{event.get('nombre', '')}{event.get('entidad', '')}{event.get('fecha', '')}"

        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    def is_duplicate_by_id(self, event: Dict) -> bool:
        """
        Verifica si un evento es duplicado basándose en su ID

        Args:
            event: Evento a verificar

        Returns:
            True si es duplicado, False en caso contrario
        """
        event_id = event.get('id') or self.generate_event_id(event)

        if event_id in self.seen_ids:
            return True

        self.seen_ids.add(event_id)
        return False

    def calculate_similarity(self, event1: Dict, event2: Dict) -> float:
        """
        Calcula la similitud entre dos eventos

        Args:
            event1: Primer evento
            event2: Segundo evento

        Returns:
            Puntuación de similitud (0-1)
        """
        # Comparar nombres
        name_similarity = SequenceMatcher(
            None,
            event1.get('nombre', '').lower(),
            event2.get('nombre', '').lower()
        ).ratio()

        # Comparar fechas
        date_match = 1.0 if event1.get('fecha') == event2.get('fecha') else 0.0

        # Comparar enlaces (si existen)
        link1 = event1.get('enlace', '')
        link2 = event2.get('enlace', '')
        link_match = 1.0 if link1 and link2 and link1 == link2 else 0.0

        # Comparar entidades
        org_match = 1.0 if event1.get('entidad') == event2.get('entidad') else 0.0

        # Peso de cada factor
        weights = {
            'name': 0.4,
            'date': 0.2,
            'link': 0.3,
            'org': 0.1
        }

        # Calcular similitud ponderada
        similarity = (
            name_similarity * weights['name'] +
            date_match * weights['date'] +
            link_match * weights['link'] +
            org_match * weights['org']
        )

        return similarity

    def find_duplicates(self, events: List[Dict]) -> List[List[int]]:
        """
        Encuentra grupos de eventos duplicados

        Args:
            events: Lista de eventos

        Returns:
            Lista de grupos de índices de eventos duplicados
        """
        duplicate_groups = []
        processed_indices = set()

        for i, event1 in enumerate(events):
            if i in processed_indices:
                continue

            duplicates = [i]

            for j, event2 in enumerate(events[i + 1:], start=i + 1):
                if j in processed_indices:
                    continue

                similarity = self.calculate_similarity(event1, event2)

                if similarity >= self.similarity_threshold:
                    duplicates.append(j)
                    processed_indices.add(j)

            if len(duplicates) > 1:
                duplicate_groups.append(duplicates)
                processed_indices.update(duplicates)

        return duplicate_groups

    def deduplicate(self, events: List[Dict], keep_first: bool = True) -> List[Dict]:
        """
        Elimina eventos duplicados de una lista

        Args:
            events: Lista de eventos
            keep_first: Si True, mantiene el primer evento de cada grupo duplicado

        Returns:
            Lista de eventos únicos
        """
        logger.info(f"Deduplicating {len(events)} events")

        # Asignar IDs si no los tienen
        for event in events:
            if 'id' not in event:
                event['id'] = self.generate_event_id(event)

        # Encontrar duplicados por ID exacto
        unique_events = []
        seen_ids = set()

        for event in events:
            event_id = event['id']
            if event_id not in seen_ids:
                unique_events.append(event)
                seen_ids.add(event_id)

        logger.info(f"After ID-based deduplication: {len(unique_events)} events")

        # Encontrar duplicados por similitud
        duplicate_groups = self.find_duplicates(unique_events)

        if duplicate_groups:
            logger.info(f"Found {len(duplicate_groups)} groups of similar events")

            # Crear conjunto de índices a eliminar
            indices_to_remove = set()
            for group in duplicate_groups:
                # Mantener el primero, eliminar el resto
                if keep_first:
                    indices_to_remove.update(group[1:])
                else:
                    indices_to_remove.update(group[:-1])

            # Filtrar eventos
            final_events = [
                event for i, event in enumerate(unique_events)
                if i not in indices_to_remove
            ]
        else:
            final_events = unique_events

        logger.info(f"After similarity-based deduplication: {len(final_events)} events")
        logger.info(f"Removed {len(events) - len(final_events)} duplicate events")

        return final_events

    def merge_duplicate_info(self, events: List[Dict]) -> Dict:
        """
        Fusiona información de eventos duplicados

        Args:
            events: Lista de eventos duplicados

        Returns:
            Evento fusionado con información combinada
        """
        if not events:
            return {}

        # Tomar el primer evento como base
        merged = events[0].copy()

        # Combinar descripciones si son diferentes
        descriptions = set()
        for event in events:
            if event.get('descripcion'):
                descriptions.add(event['descripcion'])

        if descriptions:
            merged['descripcion'] = ' | '.join(descriptions)

        # Tomar el enlace más completo
        links = [e.get('enlace', '') for e in events if e.get('enlace')]
        if links:
            merged['enlace'] = max(links, key=len)

        # Añadir metadatos sobre fusión
        merged['merged_from'] = len(events)
        merged['merged_at'] = datetime.now().isoformat()

        return merged
