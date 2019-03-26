SUIT_CONFIG = {
    'ADMIN_NAME': 'POBOT Junior Cup',
    'HEADER_DATE_FORMAT': 'l j F Y',
    'SEARCH_URL': '',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU': (
        '-',
        {
            'app': 'teams',
            'icon': 'icon-user',
            'models': ('Team', 'School', 'TeamContact')
        },
        '-',
        {
            'app': 'match',
            'icon': 'icon-chevron-right'
        },
        {
            'app': 'research',
            'icon': 'icon-chevron-right'
        },
        '-',
        {
            'app': 'event',
            'icon': 'icon-flag',
            'models': ('Planning', 'PlanningControl', 'Ranking')
        },
        {
            'app': 'display',
            'icon': 'icon-picture'
        },
        '-',
        {
            'app': 'volunteers',
            'label': "Volontaires",
            'icon': 'icon-user'
        },
        {
            'app': 'auth',
            'label': "Contrôle d'accès",
            'icon': 'icon-lock'
        }
    ),
    'LIST_PER_PAGE': 15,
}
