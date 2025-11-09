"""
Clasificador de eventos usando IA (OpenAI embeddings + clasificación)
"""
import os
from typing import List, Dict, Optional
import logging
from openai import OpenAI
import json

logger = logging.getLogger(__name__)


class EventClassifier:
    """
    Clasifica eventos según criterios temáticos del tercer sector
    """

    # Categorías definidas según objetivo general
    CATEGORIES = {
        'inclusion_laboral': 'Inclusión laboral',
        'formacion_profesional': 'Formación profesional',
        'derechos_infancia_juventud_mujeres': 'Derechos de infancia, juventud y mujeres',
        'acompanamiento_migrantes': 'Acompañamiento a migrantes',
        'cooperacion_internacional': 'Cooperación internacional y desarrollo',
        'ia_tercer_sector': 'Uso de IA y aplicaciones informáticas en el tercer sector'
    }

    # Criterios de clasificación
    CLASSIFICATION_CRITERIA = """
    Clasifica el siguiente evento en UNA de estas categorías:

    1. Inclusión laboral: Eventos sobre empleo, inserción laboral, inclusión de colectivos vulnerables en el mercado laboral
    2. Formación profesional: Cursos, talleres, capacitaciones, formación técnica o profesional
    3. Derechos de infancia, juventud y mujeres: Eventos sobre derechos de niños, jóvenes, mujeres, igualdad de género
    4. Acompañamiento a migrantes: Eventos sobre refugiados, migrantes, acogida, integración
    5. Cooperación internacional y desarrollo: Proyectos de cooperación, desarrollo internacional, ayuda humanitaria
    6. Uso de IA y aplicaciones informáticas en el tercer sector: Tecnología, IA, transformación digital en ONGs

    Evento:
    Título: {title}
    Descripción: {description}
    Entidad: {organization}

    Responde SOLO con el número de categoría (1-6).
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el clasificador

        Args:
            api_key: OpenAI API key (si no se proporciona, se toma de env)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None

        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
        else:
            logger.warning("No OpenAI API key provided, using rule-based classification only")

    def classify_event(self, event: Dict) -> str:
        """
        Clasifica un evento

        Args:
            event: Diccionario con datos del evento

        Returns:
            Categoría del evento
        """
        # Si ya tiene categoría y es válida, mantenerla
        current_category = event.get('categoria', '')
        if current_category in self.CATEGORIES.values():
            return current_category

        # Intentar clasificación con IA
        if self.client:
            try:
                category = self.classify_with_ai(event)
                if category:
                    return category
            except Exception as e:
                logger.error(f"Error in AI classification: {e}")

        # Fallback: clasificación basada en reglas
        return self.classify_with_rules(event)

    def classify_with_ai(self, event: Dict) -> Optional[str]:
        """
        Clasifica usando modelo de OpenAI

        Args:
            event: Evento a clasificar

        Returns:
            Categoría o None si falla
        """
        try:
            prompt = self.CLASSIFICATION_CRITERIA.format(
                title=event.get('nombre', ''),
                description=event.get('descripcion', ''),
                organization=event.get('entidad', '')
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un clasificador de eventos del tercer sector. Responde solo con el número de categoría."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )

            category_number = response.choices[0].message.content.strip()

            # Mapear número a categoría
            category_map = {
                '1': 'Inclusión laboral',
                '2': 'Formación profesional',
                '3': 'Derechos de infancia, juventud y mujeres',
                '4': 'Acompañamiento a migrantes',
                '5': 'Cooperación internacional y desarrollo',
                '6': 'Uso de IA y aplicaciones informáticas en el tercer sector'
            }

            return category_map.get(category_number)

        except Exception as e:
            logger.error(f"Error in AI classification: {e}")
            return None

    def classify_with_rules(self, event: Dict) -> str:
        """
        Clasificación basada en reglas y palabras clave

        Args:
            event: Evento a clasificar

        Returns:
            Categoría del evento
        """
        text = f"{event.get('nombre', '')} {event.get('descripcion', '')} {event.get('entidad', '')}".lower()

        # Palabras clave por categoría
        keywords = {
            'Inclusión laboral': ['empleo', 'laboral', 'trabajo', 'inserción', 'inclusión', 'empleabilidad', 'discapacidad'],
            'Formación profesional': ['formación', 'curso', 'taller', 'capacitación', 'formativo', 'aprendizaje', 'educación'],
            'Derechos de infancia, juventud y mujeres': ['niñ', 'infancia', 'joven', 'juventud', 'mujer', 'género', 'igualdad', 'derechos'],
            'Acompañamiento a migrantes': ['migrant', 'refugiad', 'acogida', 'integración', 'asilo', 'inmigra'],
            'Cooperación internacional y desarrollo': ['cooperación', 'desarrollo', 'internacional', 'humanitaria', 'solidaridad'],
            'Uso de IA y aplicaciones informáticas en el tercer sector': ['ia', 'inteligencia artificial', 'digital', 'tecnología', 'innovación', 'software']
        }

        # Contar coincidencias por categoría
        scores = {}
        for category, words in keywords.items():
            score = sum(1 for word in words if word in text)
            if score > 0:
                scores[category] = score

        # Devolver categoría con mayor puntuación
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]

        # Default: intentar inferir por organización
        org = event.get('entidad', '').lower()
        if 'once' in org or 'discapacidad' in org:
            return 'Inclusión laboral'
        elif 'children' in org or 'infancia' in org:
            return 'Derechos de infancia, juventud y mujeres'
        elif 'migrante' in org or 'acnur' in org or 'cear' in org:
            return 'Acompañamiento a migrantes'
        else:
            return 'Cooperación internacional y desarrollo'

    def classify_batch(self, events: List[Dict]) -> List[Dict]:
        """
        Clasifica un lote de eventos

        Args:
            events: Lista de eventos

        Returns:
            Lista de eventos con categorías asignadas
        """
        logger.info(f"Classifying {len(events)} events")

        for event in events:
            try:
                category = self.classify_event(event)
                event['categoria'] = category
            except Exception as e:
                logger.error(f"Error classifying event {event.get('nombre', 'unknown')}: {e}")
                event['categoria'] = 'Sin categorizar'

        logger.info("Classification completed")
        return events

    def is_relevant(self, event: Dict) -> bool:
        """
        Determina si un evento es relevante para los criterios del tercer sector

        Args:
            event: Evento a evaluar

        Returns:
            True si es relevante, False en caso contrario
        """
        # Clasificar el evento
        category = self.classify_event(event)
        event['categoria'] = category

        # Todos los eventos clasificados son relevantes
        return category != 'Sin categorizar'
