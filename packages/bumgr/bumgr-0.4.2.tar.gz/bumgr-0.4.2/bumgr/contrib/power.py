__all__ = ["Power"]

import json
import subprocess

from bumgr.config import ConfigError
from bumgr.contrib import BumgrPlugin, PluginSkipError
from bumgr.executable import Executable


class Power(BumgrPlugin, Executable):
    EXECUTABLE_DARWIN = "system_profiler"

    def __init__(
        self,
        command: str,
        include_commands: list[str] | None = None,
        exclude_commands: list[str] | None = None,
    ):
        super().__init__(command, include_commands, exclude_commands)
        if self.include_commands is None and self.exclude_commands is None:
            # If neither include_commands nor exclude_commands are set,
            # fall back to default behaviour where only 'backup' is
            # included.
            self.include_commands = ["backup"]

    @classmethod
    def check_config(cls, config: dict, **kwargs) -> None:
        if config != {}:
            raise ConfigError(("args", "Plugin does not support any arguments"))

    @property
    def is_active(self) -> bool:
        # Ignore this plugin if the executable can not be found
        try:
            _ = self.executable
        except FileNotFoundError:
            return False
        return super().is_active

    def get_charger_connected(self) -> bool | None:
        result = subprocess.run(
            [self.executable, "-detailLevel", "mini", "SPPowerDataType", "-json"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout)
        for values in output.get("SPPowerDataType", []):
            if values.get("_name", None) == "sppower_ac_charger_information":
                charger_connected = values.get(
                    "sppower_battery_charger_connected", None
                )
                if charger_connected is None:
                    return None
                else:
                    return charger_connected == "TRUE"
        return None

    def __enter__(self):
        charger_connected = self.get_charger_connected()
        if charger_connected is not None and not charger_connected:
            raise PluginSkipError("Charger not connected")

    def __exit__(self, *args):
        pass
