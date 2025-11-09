"""
Configuraciones para organizaciones colombianas del tercer sector
"""

COLOMBIAN_ORGANIZATIONS = [
    {
        'organization_name': 'Fundación Corona',
        'base_url': 'https://www.fundacioncorona.org',
        'events_url': 'https://www.fundacioncorona.org/es/eventos',
        'pais': 'Colombia',
        'categoria_default': 'Cooperación internacional y desarrollo',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Fundación Plan Colombia',
        'base_url': 'https://plan.org.co',
        'events_url': 'https://plan.org.co/eventos',
        'pais': 'Colombia',
        'categoria_default': 'Derechos de infancia, juventud y mujeres',
        'selectors': {
            'container': 'article, .event-card',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Aldeas Infantiles SOS Colombia',
        'base_url': 'https://www.aldeasinfantiles.org.co',
        'events_url': 'https://www.aldeasinfantiles.org.co/noticias-eventos',
        'pais': 'Colombia',
        'categoria_default': 'Derechos de infancia, juventud y mujeres',
        'selectors': {
            'container': 'article, .news-item',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Fundación Comparlante',
        'base_url': 'https://www.compartir.org',
        'events_url': 'https://www.compartir.org/eventos',
        'pais': 'Colombia',
        'categoria_default': 'Formación profesional',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'ACNUR Colombia',
        'base_url': 'https://www.acnur.org',
        'events_url': 'https://www.acnur.org/colombia/eventos',
        'pais': 'Colombia',
        'categoria_default': 'Acompañamiento a migrantes',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Save the Children Colombia',
        'base_url': 'https://www.savethechildren.org.co',
        'events_url': 'https://www.savethechildren.org.co/actualidad',
        'pais': 'Colombia',
        'categoria_default': 'Derechos de infancia, juventud y mujeres',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    },
    {
        'organization_name': 'Fundación WWB Colombia',
        'base_url': 'https://www.fundacionwwbcolombia.org',
        'events_url': 'https://www.fundacionwwbcolombia.org/eventos',
        'pais': 'Colombia',
        'categoria_default': 'Inclusión laboral',
        'selectors': {
            'container': 'article, .event',
            'title': 'h2, h3',
            'date': 'time, .date',
            'link': 'a'
        }
    }
]
