import pytest

from django.contrib.auth.models import User
from teams.models import Team, School, Grade, Category


@pytest.fixture()
def populated_db(db):
    User.objects.bulk_create([
        User(username='Fabrice'),
        User(username='FredR'),
        User(username='FredM'),
    ])

    School.objects.bulk_create((
        School(name='Collège International de Valbonne', city='SOPHIA ANTIPOLIS', zip_code='06560'),
        School(name='Lycée International de Valbonne', city='SOPHIA ANTIPOLIS', zip_code='06560'),
        School(name='Lycée St Joseph', city='HASPARREN', zip_code='64240'),
        School(name='Lycée du Pays de Soule', city='CHERAUTE', zip_code='64130'),
        School(name='Collège Louis Nucera', city='NICE', zip_code='06000'),
        School(name='Collège Emile Roux', city='LE CANNET', zip_code='06160'),
        School(name='Collège St Philippe Neri', city='JUAN LES PINS', zip_code='06110'),
        School(name='Collège Rolland Garros', city='NICE', zip_code='06000'),
    ))

    teams = []

    lycee_pays_de_soule = School.objects.get(name="Lycée du Pays de Soule")
    teams.extend([
        Team(name="Castanha Shüta", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
        Team(name="The Saving Family", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
        Team(name="Réunion Basci-Béarnais", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
    ])

    liv = School.objects.get(name="Lycée International de Valbonne")
    teams.extend([
        Team(name="Playbot", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="BRUH", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Robot Jul", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Wizzbot", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Green Studio", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Blank", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Bang Schnecke", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        Team(name="Gear", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
    ])

    civ = School.objects.get(name="Collège International de Valbonne")
    teams.extend([
        Team(name="Robot55 Team", grade=Grade.cinquieme, category=Category.Arduino, school=civ),
        Team(name="Robot56 Team", grade=Grade.cinquieme, category=Category.Arduino, school=civ),
    ])

    st_joseph = School.objects.get(name="Lycée St Joseph")
    teams.extend([
        Team(name="PoweRobot", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
        Team(name="2ndC1", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
        Team(name="SEJO Haspatech", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
        Team(name="EuskalRobota", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
        Team(name="2ndSTGA", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
    ])

    st_ph_neri = School.objects.get(name="Collège St Philippe Neri")
    teams.extend([
        Team(name="Les Nerissons", grade=Grade.sixieme, category=Category.Mindstorms, school=st_ph_neri),
    ])

    emile_roux = School.objects.get(name="Collège Emile Roux")
    teams.extend([
        Team(name="MEDITES", grade=Grade.quatrieme, category=Category.Mindstorms, school=emile_roux),
        Team(name="Club Rob", grade=Grade.cinquieme, category=Category.Arduino, school=emile_roux),
    ])

    Team.objects.bulk_create(teams)
