SUIT_CONFIG = {
    'ADMIN_NAME': 'POBOT Junior Cup',
    'HEADER_DATE_FORMAT': 'l j F Y',
    'SEARCH_URL': '',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU': (
        '-',
        {
            'app': 'teams',
            'icon': 'icon-user'
        },
        '-',
        {
            'app': 'match',
            'icon': 'icon-flag'
        },
        {
            'app': 'research',
            'icon': 'icon-bullhorn'
        },
        '-',
        {
            'app': 'event',
            'icon': 'icon-time',
            'models': ('Planning', 'PlanningControl', 'Ranking')
        },
        {
            'app': 'display',
            'icon': 'icon-film'
        },
        '-',
        {
            'app': 'auth',
            'label': "Contrôle d'accès",
            'icon': 'icon-lock'
        }
    )
}
