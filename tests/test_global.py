# -*- coding: utf-8 -*-

import pytest
from pytest_mock import mocker

from django.contrib.auth.models import User

from teams.models import *
from match.models import *
from event.models import *

__author__ = 'Eric Pascual'


@pytest.mark.django_db
def test_populated_db(populated_db):
    assert Team.objects.count() == 21
    assert Team.objects.filter(category_code=Category.Mindstorms.value).count() == 18
    assert Team.objects.filter(category_code=Category.Arduino.value).count() == 3
    assert Team.objects.values('school').distinct().count() == 6

    assert User.objects.count() == 3


@pytest.mark.django_db
def test_result_add(populated_db, mocker):
    assert not Team.objects.filter(present=True).exists()

    mocker.spy(Ranking, 'compute')
    assert Ranking.compute.call_count == 0

    # adding a result to a team should update it as automatically present
    team = Team.objects.get(num=1)
    assert not hasattr(team, 'robotics1')

    referee = User.objects.get(username='Fabrice')
    Robotics1.objects.create(team=team, referee=referee, trips=5, variants=1)
    assert hasattr(team, 'robotics1')
    assert team.present

    # it should also have triggered the global ranking update
    assert Ranking.compute.call_count == 1


@pytest.mark.django_db
def test_ranking_compute(populated_db, mocker):
    mocker.spy(Ranking, 'compute')

    team = Team.objects.get(num=1)
    referee = User.objects.get(username='Fabrice')

    for cls in (Robotics1, Robotics2, Robotics3):
        cls.objects.create(team=team, referee=referee)
        assert not Team.objects.indexable().exists()

    DocumentaryWork.objects.create(team=team)
    assert not Team.objects.indexable().exists()

    Poster.objects.create(team=team)
    assert Team.objects.indexable().exists()

    assert Ranking.compute.call_count == 5

    assert Ranking.objects.all().exists()
    assert Ranking.objects.count() == 2

    for rt_code in (RankingType.Scratch.value, team.category_code):
        ranking = Ranking.objects.get(team=team, type_code=rt_code)

        assert ranking.robotics == 1
        assert ranking.research == 1
        assert ranking.poster == 1


@pytest.mark.django_db
def test_planning(populated_db, mocker):
    team = Team.objects.get(num=1)
    referee = User.objects.get(username='Fabrice')

    Planning.objects.create(
        team=team,
        match1_time=arrow.get("12:30", "HH:mm").time(),
        match2_time=arrow.get("13:30", "HH:mm").time(),
        match3_time=arrow.get("14:30", "HH:mm").time(),
        presentation_time=arrow.get("15:30", "HH:mm").time(),
    )

    assert not any(team.planning.done)

    for cls in (Robotics1, Robotics2, Robotics3):
        cls.objects.create(team=team, referee=referee)
    assert any(team.planning.done)

    DocumentaryWork.objects.create(team=team)
    Poster.objects.create(team=team)

    assert all(team.planning.done)
