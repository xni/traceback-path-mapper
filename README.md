# Python traceback path-mapper
PyCharm is unable to deal with tracebacks from remote servers.
This is a simple script to patch Python tracebacks, replacing remote paths with local ones.

Assume that you saw an exception on you remote server.
Of course it is not your's, it is your colleague's one!
So, you want to understand that's happening as soon as possible.

First of all you are switching to the tag,
which corresponds to the version which is in production now.

![switching tag](/doc/img/switch_tag.png)

Then, you paste code of your exception traceback to this script
(having a config written already) and get a patched
traceback. I.e. original traceback was:

```pytb
Traceback (most recent call last):
  File "/usr/lib/python/dist-packages/django/core/handlers/base.py", line 1, in get_response
    response = callback(request, *callback_args, **callback_kwargs)
  File "/usr/lib/yandex/taxi-cabinet/taxicabinet/views/__init__.py", line 544, in get
    response = self.base_orders_GET_response(request)
  File "/usr/lib/yandex/taxi-cabinet/taxicabinet/views/__init__.py", line 497, in base_orders_GET_response
    (start, end) = period.split(' - ')
ValueError: need more than 1 value to unpack
```

Patch it:

```
$ cat /tmp/tb | ./patchtb.py 
Traceback (most recent call last):
  File "/usr/lib/python/dist-packages/django/core/handlers/base.py", line 1, in get_response
    response = callback(request, *callback_args, **callback_kwargs)
  File "/Users/stromsund/Development/backend/taxi-cabinet/taxicabinet/views/__init__.py", line 544, in get
    response = self.base_orders_GET_response(request)
  File "/Users/stromsund/Development/backend/taxi-cabinet/taxicabinet/views/__init__.py", line 497, in base_orders_GET_response
    (start, end) = period.split(' - ')
ValueError: need more than 1 value to unpack
```

Copy-n-Paste to `Analyze Stacktrace` window of PyCharm.

Now you can navigate through the stacktrace.

![stacktrace window](/doc/img/stackwindow.png)

_Happy debugging!_
