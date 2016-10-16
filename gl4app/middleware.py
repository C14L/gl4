import sys
import cProfile

from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from io import StringIO
from time import time
from django.conf import settings
from django.utils.translation import get_language


class FixSomeWordInflextionsMiddleware(object):
    """Some auto-added inflextions of translated words in German are off."""

    def process_response(self, request, response):
        if response.streaming:
            return response

        tr = []
        lang = get_language()

        # Use Byte string, because `response.content` is not a Unicode string.
        if lang == 'de':
            tr = (
                (b'beigee', b'beige'), (b'Beigee', b'Beige'),
                (b'beigeer', b'beiger'), (b'Beigeer', b'Beiger'),
                (b'beigeen', b'beigen'), (b'Beigeen', b'Beigen'),

                (b'rosae', b'rosane'), (b'Rosae', b'Rosane'),
                (b'rosaer', b'rosaner'), (b'Rosaer', b'Rosaner'),
                (b'rosaen', b'rosanen'), (b'Rosaen', b'Rosanen'),
            )
        elif lang == 'en':
            pass

        for x in tr:
            response.content = response.content.replace(x[0], x[1])

        return response


class ProfilerMiddleware(object):
    profiler = None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.ENABLE_PROFILER and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.ENABLE_PROFILER and 'prof' in request.GET:
            self.profiler.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response


class ExecTimeLoggerMiddleware:
    """Measure execution time and log to a file."""

    def log(self, delta, method, path):
        if not getattr(settings, 'ENABLE_TIME_LOGGER', False):
            return

        if not getattr(settings, 'TIME_LOGGER_LOGFILE', False):
            raise ImproperlyConfigured('Time logger enabled but file not set.')

        now = datetime.utcnow().isoformat()

        with open(settings.TIME_LOGGER_LOGFILE, 'a') as fh:
            fh.write('{} {} {} {}\n'.format(now, delta, method, path))

    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'exec_time_logger', time())

    def process_response(self, request, response):
        if hasattr(request, 'exec_time_logger'):
            delta = time() - request.exec_time_logger
            self.log(delta, request.method, request.path)

        return response

    def process_exception(self, request, exception):
        pass
