import datetime

__all__ = ['PJC']

PJC = {
    'brand': 'POBOT Junior Cup',
    'edition': '2019',
    'thema': 'Dependency Assistance',
    'event_date': "25/05/2019",
    'start_time': "12:30",
    'end_time': "17:30",
    'planning_slot_minutes': 10,
    'time_limits': [
        datetime.time(15, 00),  # time limit for round 1 matches
        datetime.time(16, 00),  # time limit for round 2 matches
        datetime.time(17, 00),  # time limit for round 3 matches
        datetime.time(17, 00)  # time limit for presentations
    ],
    'display_page_size': 10,
    'display_next_schedules_count': 9,
    'display_use_animations': True
}
PJC['title_long'] = ' '.join([PJC['brand'], PJC['edition']])
# print('PJC =', PJC)
