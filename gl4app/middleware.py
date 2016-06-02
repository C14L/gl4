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
