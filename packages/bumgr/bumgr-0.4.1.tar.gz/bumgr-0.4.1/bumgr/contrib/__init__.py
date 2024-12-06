__all__ = ["BumgrPlugin", "PluginSkipError", "SkippableExitStack", "plugin_loader"]


import importlib
import logging
from abc import ABCMeta
from contextlib import AbstractContextManager, ExitStack
from types import TracebackType

from bumgr.config import ConfigError, Configurable

logger = logging.getLogger("bumgr.contrib")


class BumgrPlugin(AbstractContextManager, Configurable, metaclass=ABCMeta):
    def __init__(
        self,
        command: str,
        include_commands: list[str] | None = None,
        exclude_commands: list[str] | None = None,
        **kwargs,
    ):
        self.command = command
        self.include_commands = include_commands
        self.exclude_commands = exclude_commands

    @property
    def is_active(self) -> bool:
        if self.include_commands is not None:
            return self.command in self.include_commands and self.command not in (
                self.exclude_commands or []
            )
        if self.exclude_commands is not None:
            return self.command not in self.exclude_commands
        # At this point, neither 'exclude_commands' nor 'include_commands'
        # are set, so we can just return true as no preference is specified
        return True


class PluginSkipError(InterruptedError):
    pass


class SkippableExitStack(ExitStack):
    def enter_plugin_context(self, plugin: BumgrPlugin):
        if plugin.is_active:
            self.enter_context(plugin)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
        /,
    ) -> bool:
        super().__exit__(exc_type, exc_value, traceback)
        if exc_type == PluginSkipError:
            logger.info(f"Skipped: {exc_value}")
            return True
        return False


def plugin_loader(plugin_spec: dict, command: str) -> BumgrPlugin:
    plugin_module_spec = plugin_spec.get("module", None)
    if plugin_module_spec is None:
        raise ConfigError(("module", "Field has to be set"))
    try:
        plugin_module_str, plugin_class_str = plugin_module_spec.rsplit(".", 1)
    except ValueError:
        raise ConfigError(("module", "Field is not a valid python class"))
    plugin_class: type[BumgrPlugin] | None
    try:
        plugin_class = getattr(
            importlib.import_module(plugin_module_str), plugin_class_str, None
        )
    except ModuleNotFoundError:
        plugin_class = None
    if plugin_class is None:
        raise ConfigError(("module", f"Class '{plugin_module_spec}' can not be found"))
    arguments = plugin_spec.get("args", {})
    include_commands = plugin_spec.get("include_commands", None)
    exclude_commands = plugin_spec.get("exclude_commands", None)
    plugin_class.check_config(arguments)
    return plugin_class(
        command,
        include_commands=include_commands,
        exclude_commands=exclude_commands,
        **arguments,
    )
