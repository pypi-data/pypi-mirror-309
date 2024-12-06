import typing
from pg_common import SingletonBase, log_info, KeyType
import os
import importlib

__all__ = [
           "func_decorator", "FuncDecoratorManager", "ObjDecoratorManager",
           ]
__author__ = "baozilaji@gmail.com"


class _FuncDecoratorManager(SingletonBase):
    def __init__(self):
        self._handlers: dict[str, typing.Coroutine] = {}

    def register(self, method: str, handler: typing.Coroutine):
        self._handlers[method] = handler
        log_info(f"register handler: {method}")

    def get_func(self, method: str) -> typing.Coroutine:
        return self._handlers[method] if method in self._handlers else None

    @staticmethod
    def scan_decorators(director):
        _handler_dir = director
        log_info(f"handler dirs: {_handler_dir}")

        for _root, _dirs, _files in os.walk(_handler_dir):
            for _file in _files:
                if _file.endswith(".py"):
                    _module_name = _root.replace("/", ".")
                    _module_name = f"{_module_name}.{_file[:-3]}"
                    _module = importlib.import_module(_module_name)
                    log_info(f"load handler {_module_name}")


FuncDecoratorManager = _FuncDecoratorManager()


def func_decorator(func_key: str) -> typing.Callable:
    def decorator(func: typing.Coroutine) -> typing.Coroutine:
        FuncDecoratorManager.register(func_key, func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)
        return inner
    return decorator


class _ObjDecoratorManager(SingletonBase):
    def __init__(self):
        self._objs: dict[KeyType, object] = {}

    def register(self, key: KeyType):

        def decorator(cls):
            self._objs[key] = cls()
            log_info(f"register object: {key}")
            return cls

        return decorator

    def get_obj(self, key: KeyType):
        return self._objs[key] if key in self._objs else None

ObjDecoratorManager = _ObjDecoratorManager()


