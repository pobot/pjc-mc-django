import datetime

__all__ = ['PJC']

PJC = {
    'brand': 'POBOT Junior Cup',
    'edition': '2017',
    'thema': 'Serch and rescue',
    'start_time': "12:30",
    'end_time': "17:30",
    'planning_slot_minutes': 30,
    'time_limits': [
        datetime.time(15, 00),  # time limit for round 1 matches
        datetime.time(16, 00),  # time limit for round 2 matches
        datetime.time(17, 00),  # time limit for round 3 matches
        datetime.time(17, 00)  # time limit for presentations
    ]
}
# print('PJC =', PJC)
