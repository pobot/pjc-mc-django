import pytest

from django.core.exceptions import ValidationError

from match.models import *
from teams.models import Team

pytestmark = pytest.mark.django_db


@pytest.fixture()
def team():
    """ Create a dummy team so that representing match instances in exception messages does not 
    hang because missing the mandatory team relation in involved instanes. """
    return Team(name='Foo')


def test_rob1_clean_ok(team):
    m = Robotics1(team=team, trips=2, variants=1)
    m.clean()   # should pass


def test_rob1_clean_errors(team):
    m = Robotics1(team=team, trips=2, variants=2)
    with pytest.raises(ValidationError) as context:
        m.clean()  # should fail
    assert 'trips' in context.value.message_dict
    assert 'variants' in context.value.message_dict


def test_rob1_points(team):
    m = Robotics1(team=team, trips=2, variants=1)
    assert m.get_points() == 7


def test_rob3_clean_ok(team):
    m = Robotics3(team=team, trips=2, variants=1, moved_obstacles=1)
    m.clean()   # should pass


def test_rob3_clean_errors(team):
    m = Robotics3(team=team, trips=2, variants=2)
    with pytest.raises(ValidationError) as context:
        m.clean()  # should fail
    assert 'trips' in context.value.message_dict
    assert 'variants' in context.value.message_dict

    m = Robotics3(team=team, trips=2, variants=1, moved_obstacles=3)
    with pytest.raises(ValidationError) as context:
        m.clean()  # should fail
    assert 'trips' in context.value.message_dict
    assert 'moved_obstacles' in context.value.message_dict


def test_rob3_points(team):
    m = Robotics3(team=team, trips=2, variants=1)
    assert m.get_points() == 9

    # check that the elementary value differences (e.g. trips) are properly applied
    m1 = Robotics1(team=team, trips=2, variants=1)
    assert m.get_points() != m1.get_points()

    m = Robotics3(team=team, trips=2, variants=1, moved_obstacles=2)
    assert m.get_points() == 7
