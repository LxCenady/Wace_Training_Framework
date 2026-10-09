"""Microkernel: service registry + event bus + plugin loader.

Knows nothing about maths, databases or UI. A plugin is a module in plugins/ with
setup(k); it talks to others only through k.provide/k.get (services) and k.on/k.emit (events).
"""
import importlib

_MISSING = object()


class Kernel:
    def __init__(self, root):
        self.root = root  # data folder (contains MAM/, MAS/, wace.db)
        self._services, self._handlers = {}, {}

    def provide(self, name, obj):
        self._services[name] = obj
        return obj

    def get(self, name, default=_MISSING):
        if name in self._services:
            return self._services[name]
        if default is _MISSING:
            raise KeyError(f"no plugin provides '{name}'")
        return default

    def on(self, event, fn):
        self._handlers.setdefault(event, []).append(fn)

    def emit(self, event, *args):
        for fn in list(self._handlers.get(event, ())):
            fn(*args)

    def load(self, names):
        for name in names:
            importlib.import_module(f"plugins.{name}").setup(self)
