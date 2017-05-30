# -*- coding: utf-8 -*-

import datetime
from collections import namedtuple
import logging

from django.http import JsonResponse, HttpRequest
from django.views.generic import TemplateView, View
from django.template.loader import get_template
from django.conf import settings
from django.core.paginator import Paginator

from .models import DisplaySettings, Display

from teams.models import Team
from event.models import Planning


Progression = namedtuple('Progression', 'team_name rob1 rob2 rob3 research')
StatusItem = namedtuple('StatusItem', 'status time')

logger = logging.getLogger('django.' + __name__)
logger.setLevel(logging.INFO)

logger.debug("loading content templates")
content_templates = {
    'message': get_template("display/message.html"),
    'scores': get_template("display/scores.html"),
    'planning': get_template("display/planning.html"),
    'checkin': get_template("display/checkin.html"),
    'next_schedules': get_template("display/next_schedules.html"),
}

use_animations = settings.PJC.get('display_use_animations', False)


class HomeView(TemplateView):
    template_name = "display/home.html"
    DISPLAY_TITLE = settings.PJC['title_long']

    def get_context_data(self, **kwargs):
        return {
            'title': self.DISPLAY_TITLE,
        }


class ContentProvider(object):
    title = ''

    def get_dataset(self):
        raise NotImplementedError()

    def get_context(self, data):
        raise NotImplementedError()


class CheckinContentProvider(ContentProvider):
    title = 'Arrivée des équipes'

    def get_dataset(self):
        return [
            (team.verbose_name, team.present)
            for team in Team.objects.all()
        ]

    def get_context(self, data):
        return {
            'teams': data
        }


class PlanningContentProvider(object):
    title = 'Planning'

    # tournament item statuses
    STATUS_DONE, STATUS_NOT_DONE, STATUS_LATE = range(3)

    TIME_SPAN = settings.PJC['time_limits']

    def get_dataset(self):
        now = datetime.datetime.now().time()

        def get_status(done, time):
            if done:
                return self.STATUS_DONE
            return self.STATUS_LATE if now > time else self.STATUS_NOT_DONE

        return [
            Progression(team.verbose_name, *[
                StatusItem(get_status(done, time), time)
                for time, done in zip(team.planning.times, team.planning.done)
            ])
            for team in Team.objects.filter(present=True, planning__isnull=False)
        ]

    def get_context(self, data):
        return {
            "time_limits": self.TIME_SPAN,
            "progress": data,
            "STATUS_DONE": self.STATUS_DONE,
            "STATUS_LATE": self.STATUS_LATE,
            "STATUS_NOT_DONE": self.STATUS_NOT_DONE,
        }


class ScoresContentProvider(object):
    title = 'Scores robotique'

    def get_dataset(self):
        def get_robotics_points(team, rob_num):
            attr = 'robotics%d' % rob_num
            if hasattr(team, attr):
                return getattr(team, attr).get_points()
            else:
                return ''

        teams = Team.objects.filter(present=True)

        names = [team.verbose_name for team in teams]
        points = [[get_robotics_points(team, n) for n in range(1, 4)] for team in teams]
        try:
            best_scores = [max((vv for vv in v if isinstance(vv, int))) for v in list(zip(*points))]
        except ValueError:
            # happens when there is not yet enough data for being able to compute max
            qual_points = [[(pts, False) for pts in team_points] for team_points in points]
        else:
            qual_points = [[(pts, pts == best) for pts, best in zip(team_points, best_scores)] for team_points in points]

        return list(zip(names, qual_points))

    def get_context(self, data):
        return {
            'rng123': range(1, 4),
            'scores_data': [
                {
                    'team_name': team_data[0],
                    'qpoints': team_data[1],
                }
                for team_data in data
            ]
        }


class NextSchedulesContentProvider(object):
    title = 'Prochains passages'

    LIMIT = settings.PJC.get('display_next_schedules_count', 6)

    def get_dataset(self):
        return sorted([
            {
                'team_name': p.team.verbose_name,
                'detail': dict(zip(['when', 'where', 'what'], p.next_schedule()))
            }
            for p in [p for p in Planning.objects.all() if not all(p.done)]
        ], key=lambda x: x['detail']['when'])[:self.LIMIT]

    def get_context(self, data):
        return {
            'schedules': data
        }


class ContentView(View):
    """ Handler providing the content part of the displays on TV sets.

    Th javascript code of the HTML page periodically uses this request to get the next content
    to put on the public address TV screens.
    """
    KEY_SAVED_CONTEXT = 'saved_context'
    KEY_DISPLAY_STATE = 'display_state'
    PAGE_SIZE = settings.PJC.get('display_page_size', 10)

    # tournament item statuses
    # DONE, NOT_DONE, LATE = range(3)

    content_providers = {
        'checkin': CheckinContentProvider(),
        'planning': PlanningContentProvider(),
        'scores': ScoresContentProvider(),
        'next_schedules': NextSchedulesContentProvider()
    }

    settings = None

    def get(self, request: HttpRequest, *args, **kwargs):
        self.settings = DisplaySettings.objects.first()

        # ask for the data of the next display to show
        # (name of the display and template rendering context)
        display_name, template_context = self.next_display_content(request)
        # logger.info('next_display: %s', display_name)
        # logger.info('context: %s', template_context)

        return JsonResponse(dict(
            clock=datetime.datetime.now().strftime("%H:%M:%S"),
            delay=self.settings.delay,
            use_animations=use_animations,
            content=content_templates[display_name].render(template_context)
        ))

    def next_display_content(self, request):
        """
        Computes the data for the next display to be shown.
        
        The HTTP session is used to keep the current state information, including
        the current display shown on the client.
        
        :param HttpRequest request: the incoming request 
        :return: the name of the next display and the context data for rendering it
        :rtype: tuple
        """
        display_settings = self.settings
        # convert the sequence in names since session cannot save enums
        seq = [d.name for d in display_settings.current_sequence()]
        # logger.info("seq=%s", seq)

        session = request.session
        current_display, current_page = session.pop(self.KEY_DISPLAY_STATE, (seq[0], 1))
        if current_display == Display.message.name:
            current_display, current_page = seq[0], 1
        # logger.info("current_display, current_page = %s", (current_display, current_page))

        message = display_settings.message
        if message and self.KEY_SAVED_CONTEXT not in session:
            # we have a message to include in the sequence (between 2 subsequent displays)

            # We are not yet showing it, so it will be inserted before what
            # would normally be displayed otherwise.

            # Remember the current state, for restarting from this point on next
            # cycle
            session[self.KEY_SAVED_CONTEXT] = (current_display, current_page)
            session.set_expiry(0)
            session.clear_expired()

            # returns message display related data
            return Display.message.name, dict(level='info', content=message)

        if self.KEY_SAVED_CONTEXT in session:
            # We have just displayed the message, so we restore the "normal" state
            # for running the sequence nominal computation and clear the save area
            current_display, current_page = request.session.pop(self.KEY_SAVED_CONTEXT)
            # logger.info("SAVED: current_display, current_page = %s", (current_display, current_page))
            if current_display == Display.message.name:
                current_display, current_page = seq[0], 1

        # at this point we have in current_display and current_page the state of what
        # is on the screen.

        # do we need to stay on the current display for paginate ?

        # get the displayed data, depending on the current state
        ds = self.get_display_dataset(current_display)
        paginator = Paginator(ds, per_page=self.PAGE_SIZE)

        if paginator.num_pages > current_page:
            # we need to stay on this page
            next_display = current_display
            next_page = current_page + 1

        else:
            # advance to next display in the sequence
            next_display = Display.next_in_sequence(current_display, seq, Display.planning.name)
            next_page = 1

            # get the data for the new display
            ds = self.get_display_dataset(next_display)
            paginator = Paginator(ds, per_page=self.PAGE_SIZE)

        # get the rendering context for the display to be shown
        template_context = self.get_template_context(next_display, paginator.page(next_page).object_list)
        template_context.update({
            'page_count': paginator.num_pages,
            'page_num': next_page,
        })

        # save the current state
        session[self.KEY_DISPLAY_STATE] = (next_display, next_page)

        # return the expected data
        return next_display, template_context

    def get_display_dataset(self, display):
        """
        Returns the data set to be paginated, as a list.
        
        :param str display: the name of the display which queryset is requested 
        :return: the dataset
        :rtype: list
        """
        try:
            provider = self.content_providers[display]
        except KeyError:
            logger.error("no content provider set for display '%s'", display)
            return []
        else:
            return provider.get_dataset()

    def get_template_context(self, display, data):
        """
        Returns the template rendering context for a given display and data set.
        
        :param str display: the name of the display to be rendered 
        :param list data: the data to be displayed 
        :return: the template rendering context
        :rtype: dict
        """
        try:
            provider = self.content_providers[display]
        except KeyError:
            logger.error("no content provider set for display '%s'", display)
            return []
        else:
            context = {
                'title': provider.title
            }
            context.update(provider.get_context(data))
            return context
