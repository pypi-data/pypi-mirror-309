__all__ = ["Backup"]

import json
import logging
import os
import shutil
import subprocess
import sys
from contextlib import AbstractContextManager
from os.path import expanduser, expandvars
from pathlib import Path
from tempfile import mkstemp
from typing import Any, Self

from rich.console import Console
from rich.filesize import decimal
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from bumgr.config import ConfigError, Configurable
from bumgr.executable import Executable

logger = logging.getLogger("bumgr.backup")


class Backup(AbstractContextManager, Executable, Configurable):
    EXECUTABLE = "restic"
    # For the case that homebrew is not in PATH when bumgr is run
    EXECUTABLE_DARWIN = ["restic", "/opt/homebrew/bin/restic"]
    RESTIC_PROGRESS_FPS: str = "5"

    def __init__(
        self,
        source: str,
        repository: str | None = None,
        password_file: str | None = None,
        password_command: str | None = None,
        exclude: str | list[str] | None = None,
        exclude_file: str | list[str] | None = None,
        macos_exclude_item: bool = True,
        exclude_caches: bool = True,
        hostname: str | None = None,
        use_static_hostname: bool = True,
        env: dict[str, Any] | None = None,
        pass_env_all: bool = False,
        pass_env_path: bool = True,
        pass_env_home: bool = True,
        mount: str | None = None,
        timeout: int = 1800,
    ):
        """

        :param source:
        :param repository:
        :param password_file:
        :param password_command:
        :param exclude:
        :param exclude_file:
        :param macos_exclude_item: Use ``mdutil`` command to determine
            exclude items for macOS backups. Enabled by default.
        :param exclude_caches: Pass the '--exclude-caches' to restic.
        :param hostname: Set a hostname explicitly.
        :param use_static_hostname: Determine the static hostname. Works
            on macOS and Linux. This hostname usually never changes
            when connecting to different networks. Ignored if
            ``hostname``is set. Enabled by default.
        :param env: Optional dictionary of additional environment
            variables. Note that these environment variable are only
            passed to restic, but are not available to expand paths.
        :param pass_env_all: Whether all environment variables that are
            set when running this program are passed to restic.
            Defaults is ``False``.
        :param pass_env_path: Whether the 'PATH' environment is passed
            to restic. Needed for password commands.
            Default is ``True``. Ignored if :param:`pass_env_all`
            is ``True``.
        :param pass_env_home: Whether the 'HOME' environment is passed
            to restic. Needed for using cache. Default is ``True``.
            Ignored if :param:`pass_env_all` is ``True``.
        :param mount: Mount point
        :param timeout: Timeout for the backup process.
            Defaults to 1800 (30 min).
        """
        self.repository = repository
        self.source = source
        self.password_file = password_file
        self.password_command = password_command
        self.exclude = (
            exclude if isinstance(exclude, list) or not exclude else [exclude]
        )
        self.exclude_file = (
            exclude_file
            if isinstance(exclude_file, list) or not exclude_file
            else [exclude_file]
        )
        self.macos_exclude_item = macos_exclude_item and os.uname()[0] == "Darwin"
        self._macos_exclude_temp_file: str | None = None
        self._hostname = hostname
        self.use_static_hostname = use_static_hostname
        self._env = env
        self.pass_env_all = pass_env_all
        self.pass_env_path = pass_env_path
        self.pass_env_home = pass_env_home
        self.mount_point = mount
        self.exclude_caches = exclude_caches
        self.timeout = timeout

    def __enter__(self) -> Self:
        if self.macos_exclude_item:
            handle, self._macos_exclude_temp_file = mkstemp()
            logger.debug(f"Created temporary file '{self._macos_exclude_temp_file}'")
            with os.fdopen(handle) as f:
                # Retrieve backup exclude items from 'mdfind' and write them
                # in the temporary file.
                logger.debug("Writing temporary exclude items...")
                subprocess.run(
                    ["mdfind", "com_apple_backup_excludeItem = 'com.apple.backupd'"],
                    stdout=f,
                    check=True,
                )
            # Temporary file can be closed because the file is passed as a
            # filename to 'restic'
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback, /):
        if self.macos_exclude_item:
            if self._macos_exclude_temp_file is None:
                logger.warning(
                    "Expected a temporary file for exclude items "
                    "but variable is 'None'"
                )
            else:
                temp_file_path = Path(self._macos_exclude_temp_file)
                if not temp_file_path.exists():
                    logger.warning(
                        f"Temporary file '{self._macos_exclude_temp_file}' "
                        "does not exist anymore"
                    )
                else:
                    # Remove the file using 'unlink'
                    temp_file_path.unlink()
                    logger.debug("Removed temporary file used for exclude items")

    @property
    def hostname(self) -> str | None:
        if self._hostname:
            return self._hostname
        if not self.use_static_hostname:
            return None
        sysname = os.uname()[0]
        if sysname == "Darwin":
            result = subprocess.run(
                ["scutil", "--get", "LocalHostName"], capture_output=True, text=True
            )
            return result.stdout.strip()
        elif sysname == "Linux" and shutil.which("hostnamectl") is not None:
            result = subprocess.run(
                ["hostnamectl", "--static"], capture_output=True, text=True
            )
            return result.stdout.strip()
        return None

    @property
    def _hostname_args(self) -> tuple[str, str] | tuple:
        hostname = self.hostname
        if hostname is None:
            return ()
        else:
            return ("--host", hostname)

    @property
    def _exclude_args(self) -> list[str]:
        args = []
        if self.exclude:
            for exclude in self.exclude:
                args.append("--exclude")
                args.append(exclude)
        if self.exclude_file:
            for exclude_file in self.exclude_file:
                args.append("--exclude-file")
                args.append(self._expand_path(exclude_file))
        if self.macos_exclude_item:
            if self._macos_exclude_temp_file is None:
                raise RuntimeError(
                    "'_macos_exclude_temp_file' is 'None' but should be set."
                )
            args.append("--exclude")
            args.append(self._macos_exclude_temp_file)
        if self.exclude_caches:
            args.append("--exclude-caches")
        return args

    @property
    def _password_args(self) -> tuple[str, str] | tuple:
        match (self.password_file, self.password_command):
            case (str(password_file), None):
                return ("--password-file", self._expand_path(password_file))
            case (None, str(password_command)):
                return ("--password-command", password_command)
            case (None, None):
                return ()
            case _:
                # There are many possibilities: Either both values are
                # set, but this should have been checked before. It is
                # also possible that neither values are of type str.
                # Eitherway, a ConfigError should be raised.
                raise ConfigError(
                    (
                        "password_file, password_command",
                        "Invalid values for 'password_file' and 'password_command'. "
                        "Only one of the attributes can be set at a time "
                        "and it has to be a valid string.",
                    )
                )

    @staticmethod
    def _expand_path(path: str) -> str:
        """Expands a given path to resolve variables like $HOME and
        user directories indicated by '~'.
        """
        return expanduser(expandvars(path))

    @property
    def _repo_args(self) -> tuple[str, str] | tuple:
        if self.repository is not None:
            return ("--repo", self._expand_path(self.repository))
        else:
            return ()

    @property
    def env(self) -> dict:
        envs: dict[str, str | None] = dict()
        if self.pass_env_all:
            envs.update(os.environ)
        else:
            if self.pass_env_path:
                envs["PATH"] = os.getenv("PATH")
            if self.pass_env_home:
                envs["HOME"] = os.getenv("HOME", expanduser("~"))
        if self._env is not None:
            envs.update(self._env)
        return envs

    def run_command(self, command: str, name: str, console: Console) -> bool:
        match command:
            case "init":
                return self.init(name, console)
            case "backup":
                return self.backup(name, console)
            case "mount":
                return self.mount(name, console)
            case "env":
                # cli_env does not need a name or console
                # so it is omitted
                return self.cli_env()
        return False

    @classmethod
    def check_config(
        cls, config: dict, command: str | None = "backup", **kwargs
    ) -> None:
        errors: list[tuple[str, str]] = []
        if not config.get("source", None):
            errors.append(("source", "Field has to be set"))
        env: dict = config.get("env", {})
        if not isinstance(env, dict):
            errors.append(("env", f"Expected type 'dict' but got '{type(env)}'"))
            env = {}
        for key, val in env.items():
            if not isinstance(val, str | bytes):
                errors.append(
                    (
                        f"env.{key}",
                        f"Expected type 'str' or 'bytes' but got '{type(val)}'",
                    )
                )
        # Create a new dictionary that contains both env and envrion.
        # Used to later check if some fields are present as an
        # environment variable.
        complete_env = {}
        complete_env.update(env)
        complete_env.update(os.environ)
        # Check if 'repository' is set
        if not config.get("repository"):
            if complete_env.get("RESTIC_REPOSITORY", None) is None:
                errors.append(("repository", "Field has to be set"))
            else:
                logger.info("Using environment variable to retrieve repository")
        # Check if the 'password_*' fields are set and mutually exclusive
        password_file = config.get("password_file")
        password_command = config.get("password_command")
        if password_file and password_command:
            errors.append(
                ("password_file, password_command", "Fields are mutually exclusive")
            )
        if (not password_file) and (not password_command):
            if (
                complete_env.get("RESTIC_PASSWORD_COMMAND") is None
                and complete_env.get("RESTIC_PASSWORD_FILE") is None
            ):
                errors.append(
                    (
                        "password_file, password_command",
                        "One of the fields has to be set",
                    )
                )
            else:
                logger.info(
                    "Using environment variables to retrieve password file or command."
                )
        timeout: int = config.get("timeout", 1800)
        if not isinstance(timeout, int):
            errors.append(("timeout", f"Expected type 'int' but got '{type(timeout)}'"))
        if command == "mount":
            if not config.get("mount"):
                errors.append(
                    (
                        "mount",
                        "Field has to be set, or use command line argument instead",
                    )
                )
        if errors:
            raise ConfigError(errors)

    def cli_env(self) -> bool:
        vars = {}
        if self.repository is not None:
            vars["RESTIC_REPOSITORY"] = self._expand_path(self.repository)
        if self.password_file is not None:
            vars["RESTIC_PASSWORD_FILE"] = self._expand_path(self.password_file)
        if self.password_command is not None:
            vars["RESTIC_PASSWORD_COMMAND"] = self.password_command
        if self._env is not None:
            vars.update(self._env)
        text = " ".join(f'{env}="{val}"' for env, val in vars.items())
        sys.stdout.write(text)
        return True

    def init(self, name: str, console: Console) -> bool:
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "init",
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        subprocess.run(args, env=self.env)
        return True

    def mount(self, name: str, console: Console) -> bool:
        if self.mount_point is None:
            raise ConfigError(
                ("mount", "Field has to be set, or use command line argument instead")
            )
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "mount",
            self._expand_path(self.mount_point),
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        try:
            subprocess.run(args, check=True, env=self.env)
        except KeyboardInterrupt:
            pass
        return True

    def backup(self, name: str, console: Console) -> bool:
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "backup",
            self._expand_path(self.source),
            *self._exclude_args,
            *self._hostname_args,
            "--json",
            "--no-scan",
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.fields[total_size]}"),
            TimeElapsedColumn(),
            TextColumn("{task.fields[errors]} errors"),
            console=console,
        )
        with progress:
            task = progress.add_task(name, total=None, errors=0, total_size=0)
            with subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                env={"RESTIC_PROGRESS_FPS": "5", **self.env},
            ) as p:
                while p.poll() is None:
                    if p.stdout is None:
                        # Check so that the type checker is happy.
                        # 'Popen.stdout' can be None or IO.
                        continue
                    else:
                        line: str = p.stdout.readline().decode("utf-8")
                        if not line.startswith("{"):
                            if line.strip():
                                logger.warning(line)
                            continue
                    try:
                        msg: dict[str, Any] = json.loads(line)
                    except json.JSONDecodeError:
                        logger.warning(f"{line}")
                        continue
                    match msg.get("message_type"):
                        case "status":
                            progress.update(
                                task,
                                total_size=decimal(int(msg.get("bytes_done", 0))),
                                errors=msg.get("error_count", 0),
                            )
                        case "error":
                            err_msg = msg.get("error", {}).get("message")
                            err_during = msg.get("during")  # noqa
                            err_item = msg.get("item")
                            output = f"Error ({name}): {err_msg} ({err_item})"
                            logger.error(output)
                            console.print(output)
                        case "summary":
                            files_new = msg.get("files_new")
                            dirs_new = msg.get("dirs_new")  # noqa: F841
                            files_changed = msg.get("files_changed")  # noqa: F841
                            dirs_changed = msg.get("dirs_changed")  # noqa: F841
                            data_added = msg.get("data_added", 0)  # noqa: F841
                            data_added_packed = msg.get("data_added_packed", 0)
                            total_duration = msg.get("total_duration")  # noqa: F841
                            table = Table(
                                "Files added",
                                "Files changed",
                                "Dirs added",
                                "Dirs changed",
                                "Data added",
                                "Data added (compressed)",
                                title="Summary",
                            )
                            table.add_row(
                                str(files_new),
                                str(files_changed),
                                str(dirs_new),
                                str(dirs_changed),
                                str(decimal(data_added)),
                                str(decimal(data_added_packed)),
                            )
                            console.print(table)

        match p.returncode:
            case 0:
                logger.info("Backup finished successfully")
                return True
            case 1:
                raise ValueError("Restic command error")
            case 2:
                raise RuntimeError()
            case 3:
                logger.warning("Restic failed to read some data")
                return True
            case 10:
                err = "Repository not found"
            case 11:
                err = "Failed to lock repository"
            case 12:
                err = "Wrong password"
            case 130:
                raise InterruptedError()
            case code:
                raise ValueError(f"Unknown error code: {code}")
        console.print(f"[red]{err}[/red]")
        logger.error(err)
        return False
