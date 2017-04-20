import pytest

from django.core.exceptions import ValidationError

from teams.models import Team, School, Grade, Category

pytestmark = pytest.mark.django_db


def test_create_valid_team():
    team = Team(name='Team1', grade=Grade.sixieme)
    team.full_clean()

    assert team.grade.bonus == Grade.sixieme.bonus
    assert team.category == Category.Mindstorms
    assert team.num is None

    team.save()
    assert team.num == 1


def test_create_invalid_team():
    team = Team()

    with pytest.raises(ValidationError) as context:
        team.full_clean()
    assert 'name' in context.value.message_dict


def test_create_valid_school():
    school = School.objects.create(name='CIV', city='SOPHIA-ANTIPOLIS', zip_code='06560')
    school.full_clean()


def test_create_invalid_school():
    school = School()
    with pytest.raises(ValidationError) as context:
        school.full_clean()
    assert 'name' in context.value.message_dict

    school = School(name='CIV')
    with pytest.raises(ValidationError) as context:
        school.full_clean()
    assert 'city' in context.value.message_dict

    school = School(name='CIV', city='SOPHIA-ANTIPOLIS')
    with pytest.raises(ValidationError) as context:
        school.full_clean()
    assert 'zip_code' in context.value.message_dict


def test_connect_team_and_school():
    civ = School.objects.create(name='CIV', city='SOPHIA-ANTIPOLIS', zip_code='06560')

    team = Team.objects.create(name='Team CIV 1', school=civ, grade=Grade.cinquieme)

    assert civ.teams.filter(pk=team.pk).exists()
    assert civ.teams.count() == 1

    Team.objects.create(name='Team CIV 2', school=civ, grade=Grade.sixieme)
    assert civ.teams.count() == 2
