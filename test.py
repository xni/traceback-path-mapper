import unittest

import patchtb


class MainTest(unittest.TestCase):
    class OutputStreamMock(object):
        def __init__(self):
            self._r = []

        def write(self, string):
            self._r.append(string)

        def result(self):
            return ''.join(self._r)

    def test_patch(self):
        input_stream = """\
Traceback (most recent call last):
  File "/usr/lib/python/dist-packages/django/core/handlers/base.py", line 1, in get_response
    response = callback(request, *callback_args, **callback_kwargs)
  File "/usr/lib/yandex/taxi-cabinet/taxicabinet/views/internal.py", line 456, in _filter_frauds
    for license in doc['licenses']:
KeyError: 'licenses'
""".splitlines(True)
        output = """\
Traceback (most recent call last):
  File "/usr/lib/python/dist-packages/django/core/handlers/base.py", line 1, in get_response
    response = callback(request, *callback_args, **callback_kwargs)
  File "/Users/stromsund/Development/backend/taxi-cabinet/taxicabinet/views/internal.py", line 456, in _filter_frauds
    for license in doc['licenses']:
KeyError: 'licenses'
"""
        config = [
            ('/usr/lib/yandex/', '/Users/stromsund/Development/backend/')
        ]
        output_stream = MainTest.OutputStreamMock()
        patchtb.patch_traceback(input_stream, output_stream, config)
        self.assertEqual(output_stream.result(), output)

