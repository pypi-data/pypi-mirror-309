import tomllib

import pytest

from bumgr.contrib import BumgrPlugin, plugin_loader


class BumgrPluginTest(BumgrPlugin):
    """Plugin class used for testing. Implements all abstract methods
    such that the plugin can be instanciated.
    """

    def __init__(
        self,
        command: str,
        include_commands: list[str] | None = None,
        exclude_commands: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(command, include_commands, exclude_commands, **kwargs)
        self.kwargs = kwargs

    def __enter__(self):
        # noop
        pass

    def __exit__(self, exc_type, exc_value, traceback, /):
        # noop
        pass

    @classmethod
    def check_config(cls, config: dict, **kwargs) -> None:
        # noop
        pass


@pytest.mark.parametrize(
    "inc, excl, res",
    [
        (None, None, True),
        (["test", "other"], None, True),
        (["other", "second"], None, False),
        (["test", "other"], ["other"], True),
        (["test", "other"], ["test"], False),
        (None, ["test"], False),
        (["other", "second"], ["test"], False),
        (["other", "second"], ["other"], False),
        (None, ["other"], True),
    ],
)
def test_plugin_is_active(inc, excl, res):
    plugin = BumgrPluginTest("test", include_commands=inc, exclude_commands=excl)
    assert plugin.is_active == res


def test_plugin_loader():
    tomlfile = """
        [[plugins]]
        module = "tests.test_plugin.BumgrPluginTest"
        include_commands = ["backup", "init", "mount"]
        [plugins.args]
        some_arg = true
        foo = 42
    """
    config = tomllib.loads(tomlfile)
    plugin_spec = config["plugins"][0]
    command = "test"
    plugin = plugin_loader(plugin_spec, command)
    assert type(plugin).__name__ == BumgrPluginTest.__name__
    assert plugin.command == "test"
    assert plugin.kwargs == {"some_arg": True, "foo": 42}
    assert plugin.include_commands == ["backup", "init", "mount"]
    assert plugin.exclude_commands is None
