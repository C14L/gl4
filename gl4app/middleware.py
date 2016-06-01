

class FixSomeWordInflextionsMiddleware(object):
    """Some auto-added inflextions of translated words in German are off."""

    def process_response(self, request, response):
        if response.streaming:
            return response

        # Use Bytes, because `response.content` is Bytes, not a Unicode string.
        tr = ((b'beigeer', b'beiger'), (b'beigee', b'beige'),
              (b'Beigeer', b'Beiger'), (b'Beigee', b'Beige'),
              (b'rosaer', b'rosaner'), (b'rosae', b'rosane'),
              (b'Rosaer', b'Rosaner'), (b'Rosae', b'Rosane'), )

        for x in tr:
            response.content = response.content.replace(x[0], x[1])

        return response

