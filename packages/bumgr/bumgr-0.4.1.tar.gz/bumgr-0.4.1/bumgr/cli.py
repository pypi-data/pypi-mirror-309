__all__ = ["cli", "BumgrCli"]


import argparse
import logging
import sys
import tomllib
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.padding import Padding

from bumgr import __version__
from bumgr.backup import Backup
from bumgr.config import ConfigError, get_config
from bumgr.contrib import BumgrPlugin, SkippableExitStack, plugin_loader

logger = logging.getLogger("bumgr.cli")


def cli():
    BumgrCli().run()


class BumgrCli:
    _BACKUP_HELP_TEXT = "name of the backup (as specified in the config)."
    DEFAULT_LOG_LEVEL = logging.CRITICAL
    NO_PLUGIN_COMMANDS = ["env"]
    SINGLE_BACKUP_COMMANDS = ["env", "init", "mount"]

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            prog="bumgr",
            description="Manage backups with restic on macOS and Linux",
        )
        self._subparsers = self._parser.add_subparsers(required=True, dest="command")
        self._args: argparse.Namespace | None = None
        self._console: Console | None = None

        self._has_config_errors: bool = False

        self._config: dict[str, Any] | None = None
        self._global_plugins: list[BumgrPlugin] | None = None
        self._backups: dict[str, tuple[Backup, list[BumgrPlugin]]] | None = None

        self.setup_parser()
        self.setup_logging()

    def setup_parser(self):
        self._parser.add_argument(
            "--version", action="version", version=f"%(prog)s {__version__}"
        )
        self._parser.add_argument(
            "-c",
            "--config",
            dest="config_file",
            type=Path,
            default=None,
            help="path of the config file.",
        )
        self._parser.add_argument(
            "-v",
            "--verbose",
            dest="log_level",
            action="count",
            default=0,
            help="more verbose output (-vvvv includes debug messages)",
        )
        self._parser.add_argument(
            "-l",
            "--log-file",
            type=Path,
            dest="log_file",
            help="optional log file to redirect log output.",
        )
        self._parser.add_argument(
            "--no-cli",
            dest="no_cli",
            default=False,
            action="store_true",
            help="disable interactive features and only ouput logs.",
        )
        self._parser.add_argument(
            "--no-color",
            dest="color",
            default=True,
            action="store_false",
            help="disable color output.",
        )
        self._setup_command_backup()
        self._setup_command_mount()
        self._setup_command_init()
        self._setup_command_env()

    def _setup_command_backup(self):
        backup_parser = self._subparsers.add_parser("backup", help="Perform backups")
        backup_parser.add_argument(
            "backup",
            nargs="*",
            action="extend",
            default=[],
            help=f"optional {self._BACKUP_HELP_TEXT}",
        )

    def _setup_command_mount(self):
        mount_parser = self._subparsers.add_parser("mount", help="Mount a backup")
        mount_parser.add_argument("backup", help=self._BACKUP_HELP_TEXT)
        mount_parser.add_argument(
            "mount_dir",
            metavar="directory",
            nargs="?",
            help=(
                "optional mount directory. "
                "If no directory is specified, "
                "the directory is taken from the configuration file."
            ),
        )

    def _setup_command_init(self):
        init_parser = self._subparsers.add_parser("init", help="Initialize a backup")
        init_parser.add_argument("backup", help=self._BACKUP_HELP_TEXT)

    def _setup_command_env(self):
        env_parser = self._subparsers.add_parser(
            "env", help="Output config as environment variables"
        )
        env_parser.add_argument("backup", help=self._BACKUP_HELP_TEXT)

    @property
    def args(self):
        if self._args is None:
            self._args = self._parser.parse_args()
        return self._args

    @property
    def command(self) -> str:
        return self.args.command

    @property
    def console(self) -> Console:
        if self._console is None:
            self._console = Console(
                no_color=not self.args.color,
                quiet=self.args.no_cli or self.command == "env",
            )
        return self._console

    def setup_logging(self):
        if not self.args.log_file:
            logging_console = Console(no_color=not self.args.color)
            logging.basicConfig(
                level=self.get_log_level(),
                handlers=[RichHandler(console=logging_console)],
            )
        else:
            logging.basicConfig(level=self.get_log_level(), filename=self.args.log_file)

    def get_log_level(self) -> int:
        if self.command == "env":
            return logging.CRITICAL
        set_level = self.DEFAULT_LOG_LEVEL - int(self.args.log_level) * 10
        return min(logging.CRITICAL, max(set_level, logging.DEBUG))

    def get_config_file(self) -> Path:
        return get_config(self.args.config_file)

    def fail(self, msg: str | None = None, code: int = 1):
        if msg is not None:
            self.console.print(msg)
            logger.error(msg)
        sys.exit(code)

    def print_config_error(self, ctx: str, err: ConfigError | str):
        self.console.print(f"[red]Config error in [underline]{ctx}[/underline]:[/red]")
        self.console.print(Padding(err, (1, 4)))
        logger.error(f"Config error in {ctx}: {err}")

    @property
    def requested_backup(self) -> list[str]:
        if isinstance(self.args.backup, list):
            if len(self.args.backup) == 0:
                return ["all"]
            return self.args.backup
        else:
            return [self.args.backup]

    def is_requested(self, backup_name: str) -> bool:
        return backup_name in self.requested_backup or "all" in self.requested_backup

    def _check_requested_backup_valid(self):
        valid_backups: set = set(self.backups.keys())
        if self.command == "backup":
            # Only allow 'all' if the command allows multiple backups
            valid_backups.add("all")
        invalid_backups: set = set(self.requested_backup) - valid_backups
        if len(invalid_backups) != 0:
            if len(invalid_backups) == 1:
                text = f"Unknown backup {invalid_backups.pop()}"
            else:
                text = f"Unknown backups {invalid_backups}"
            self.fail(f"{text}. Valid backups are: {list(valid_backups)}", code=2)

    def check(self):
        # Make sure both properties are fully evaluated and the config
        # if fully loaded.
        _ = self.global_plugins
        _ = self.backups
        if self._has_config_errors:
            # No need for an error message, the errors were already
            # reported when loading the config.
            self.fail()
        self._check_requested_backup_valid()

    @property
    def no_plugins(self) -> bool:
        return self.command in self.NO_PLUGIN_COMMANDS

    @property
    def single_backup(self) -> bool:
        return self.command in self.SINGLE_BACKUP_COMMANDS

    def run(self):
        try:
            self._run()
        except Exception as e:
            logger.debug("Exception raised in 'run'", exc_info=True)
            self.fail(f"Uncaught exception: {e}")

    def _run(self):
        self.check()
        backups = {
            name: val for name, val in self.backups.items() if self.is_requested(name)
        }
        errors = []
        with SkippableExitStack() as exit_stack:
            if not self.no_plugins:
                for plugin in self.global_plugins:
                    exit_stack.enter_plugin_context(plugin)
            for backup_name, (backup, plugins) in backups.items():
                with SkippableExitStack() as backup_exit_stack:
                    if not self.no_plugins:
                        for plugin in plugins:
                            backup_exit_stack.enter_plugin_context(plugin)
                    backup_exit_stack.enter_context(backup)
                    success = backup.run_command(
                        self.command, backup_name, self.console
                    )
                    if not success:
                        errors.append(backup_name)
                    if self.single_backup:
                        break
        if errors:
            err = f"The following backups exited with an error: {', '.join(errors)}"
            logger.error(err)
            self.console.print(f"[red]{err}[/red]")

    @property
    def config(self) -> dict[str, Any]:
        if self._config is None:
            config_path = self.get_config_file()
            logger.debug(f"Using config file '{config_path}'...")
            with config_path.open("rb") as config_file:
                try:
                    self._config = tomllib.load(config_file)
                except tomllib.TOMLDecodeError as err:
                    self.fail(f"Error while reading {config_path}: {err}")
        # mypy does not follow 'self.fail' and sees that it will exit,
        # so for mypy, the except block has no valid return value and
        # 'self._config' would still be 'None'. We can ignore the type
        # checking for this return, as at this point 'self._config' has
        # to be of type 'dict[str, Any]'.
        return self._config  # type: ignore

    @property
    def global_plugins(self) -> list[BumgrPlugin]:
        if self._global_plugins is not None:
            return self._global_plugins
        # else load all plugins from the config
        self._global_plugins = []
        for plugin in self.config.get("plugins", []):
            try:
                self._global_plugins.append(plugin_loader(plugin, self.command))
            except ConfigError as err:
                self._has_config_errors = True
                self.print_config_error("plugins", err)
        return self.global_plugins

    @property
    def backups(self) -> dict[str, tuple[Backup, list[BumgrPlugin]]]:
        if self._backups is not None:
            return self._backups
        # else load the backups from the config
        self._backups = {}
        mount_dir = getattr(self.args, "mount_directory", None)
        for backup_name, backup in self.config.get("backups", {}).items():
            if backup_name == "all":
                # Disallow name 'all'
                self._has_config_errors = True
                self.print_config_error(
                    f"backups.{backup_name}", "name 'all' is reserved"
                )
                continue
            backup_plugins: list[BumgrPlugin] = []
            for plugin in backup.pop("plugins", []):
                try:
                    backup_plugins.append(plugin_loader(plugin, self.command))
                except ConfigError as err:
                    self._has_config_errors = True
                    self.print_config_error(f"backups.{backup_name}.plugins", err)
                    continue
            if mount_dir:
                # Overwrite mount directory with the one given as a
                # command-line parameter
                backup["mount"] = mount_dir
            try:
                # Only specify the command if the backup is actually requested
                _cmd_name = self.command if self.is_requested(backup) else None
                Backup.check_config(backup, command=_cmd_name)
                self._backups[backup_name] = (Backup(**backup), backup_plugins)
            except ConfigError as err:
                self._has_config_errors = True
                self.print_config_error(f"backups.{backup_name}", err)
        return self._backups
