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


import sys
import cProfile
from io import StringIO


class ProfilerMiddleware(object):
    profiler = None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if 'prof' in request.GET:
            self.profiler.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response
