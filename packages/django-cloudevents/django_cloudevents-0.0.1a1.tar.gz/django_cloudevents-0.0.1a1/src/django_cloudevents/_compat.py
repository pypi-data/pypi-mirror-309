import django
from asgiref.sync import sync_to_async
from django.dispatch import Signal as _DjangoSignal

if django.VERSION >= (5, 0):
    Signal = _DjangoSignal
else:

    class Signal(_DjangoSignal):  # type: ignore[no-redef]
        async def asend(self, *args, **kwargs):
            return await sync_to_async(self.send)(*args, **kwargs)


__all__ = [
    "Signal",
]
