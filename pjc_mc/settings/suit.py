import os

SUIT_CONFIG = {
    'ADMIN_NAME': 'POBOT Junior Cup',
    'HEADER_DATE_FORMAT': 'l j F Y',
    'SEARCH_URL': '',
    'MENU_OPEN_FIRST_CHILD': True,
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
            'icon': 'icon-th-list',
            'models': (
                {'model': 'match.Robotics1', 'label': 'Epreuve 1'},
                {'model': 'match.Robotics2', 'label': 'Epreuve 2'},
                {'model': 'match.Robotics3', 'label': 'Epreuve 3'},
            )
        },
        {
            'app': 'research',
            'icon': 'icon-picture',
        },
        '-',
        {
            'app': 'event',
            'icon': 'icon-flag',
            'models': ('Planning', 'PlanningControl', 'Ranking')
        },
        '-',
        {
            'app': 'display',
            'icon': 'icon-film'
        },
        '-',
        {
            'app': 'volunteers',
            'icon': 'icon-heart',
            'url': 'volunteers.Volunteer',
        },
        '-',
        {
            'app': 'auth',
            'label': "Contrôle d'accès",
            'icon': 'icon-lock'
        }
    ),
    'LIST_PER_PAGE': int(os.environ.get('SUIT_LIST_PER_PAGE', "15")),
}
