from __future__ import annotations

import logging
import re

from contextlib import suppress
from importlib import import_module
from typing import TYPE_CHECKING
from typing import cast

from cleo.application import Application as BaseApplication
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from cleo.exceptions import CleoError
from cleo.formatters.style import Style
from cleo.io.null_io import NullIO
from cleo.io.outputs.output import Verbosity

from openfund.__version__ import __version__
from openfund.console.command_loader import CommandLoader
from openfund.console.commands.command import Command


if TYPE_CHECKING:
    from collections.abc import Callable

    from cleo.events.event import Event
    from cleo.io.inputs.argv_input import ArgvInput
    from cleo.io.inputs.definition import Definition
    from cleo.io.inputs.input import Input
    from cleo.io.io import IO
    from cleo.io.outputs.output import Output
    from crashtest.solution_providers.solution_provider_repository import (
        SolutionProviderRepository,
    )

    from openfund.console.commands.installer_command import InstallerCommand
    from openfund.pyopenfund import Openfund


def load_command(name: str) -> Callable[[], Command]:
    def _load() -> Command:
        # print(
        #     "----------------------- load_command %s starting...  -----------------------"
        #     % name
        # )
        words = name.split(" ")
        module = import_module("openfund.console.commands." + ".".join(words))
        command_class = getattr(module, "".join(c.title() for c in words) + "Command")
        command: Command = command_class()
        # print(
        #     "----------------------- load_command %s done! -----------------------"
        #     % name
        # )
        return command

    return _load


COMMANDS = [
    "about",
    "config",
]
"""
以下是可用命令列表：
- "add": 添加命令
- "build": 构建命令
- "check": 检查命令
- "config": 配置命令
- "init": 初始化命令
- "install": 安装命令
- "lock": 锁定命令
- "new": 新建命令
- "publish": 发布命令
- "remove": 移除命令
- "run": 运行命令
- "search": 搜索命令
- "shell": Shell命令
- "show": 显示命令
- "update": 更新命令
- "version": 版本命令
- "cache clear": 清除缓存命令
- "cache list": 列出缓存命令
- "debug info": 调试信息命令
- "debug resolve": 调试解析命令
- "env info": 环境信息命令
- "env list": 环境列表命令
- "env remove": 移除环境命令
- "env use": 使用环境命令
- "self add": 自我添加命令
- "self install": 自我安装命令
- "self lock": 自我锁定命令
- "self remove": 自我移除命令
- "self update": 自我更新命令
- "self show": 自我显示命令
- "self show plugins": 自我显示插件命令
- "source add": 源添加命令
- "source remove": 源移除命令
- "source show": 源显示命令
"""


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__("openfund", __version__)

        self._openfund: Openfund | None = None
        self._io: IO | None = None
        self._disable_plugins = False
        self._disable_cache = False
        self._plugins_loaded = False

        dispatcher = EventDispatcher()
        dispatcher.add_listener(COMMAND, self.register_command_loggers)
        dispatcher.add_listener(COMMAND, self.configure_env)
        dispatcher.add_listener(COMMAND, self.configure_installer_for_event)
        self.set_event_dispatcher(dispatcher)
        print(
            "----------------------- Application.__init__ load_command starting...  -----------------------"
        )
        command_loader = CommandLoader({name: load_command(name) for name in COMMANDS})
        print(
            "----------------------- Application.__init__ load_command done!  -----------------------"
        )
        self.set_command_loader(command_loader)

    @property
    def openfund(self) -> Openfund:
        from pathlib import Path

        from openfund.factory import Factory

        print(
            "----------------------- openfund init starting...  -----------------------"
        )
        if self._openfund is not None:
            return self._openfund

        project_path = Path.cwd()

        if self._io and self._io.input.option("directory"):
            project_path = self._io.input.option("directory")

        self._openfund = Factory().create_openfund(
            cwd=project_path,
            io=self._io,
            disable_plugins=self._disable_plugins,
            disable_cache=self._disable_cache,
        )
        print("----------------------- openfund init done...  -----------------------")
        return self._openfund

    @property
    def command_loader(self) -> CommandLoader:
        command_loader = self._command_loader
        assert isinstance(command_loader, CommandLoader)
        return command_loader

    def reset_openfund(self) -> None:
        self._openfund = None

    def create_io(
        self,
        input: Input | None = None,
        output: Output | None = None,
        error_output: Output | None = None,
    ) -> IO:
        print("----------------------- create_io starting...  -----------------------")
        io = super().create_io(input, output, error_output)

        # Set our own CLI styles
        formatter = io.output.formatter
        formatter.set_style("c1", Style("cyan"))
        formatter.set_style("c2", Style("default", options=["bold"]))
        formatter.set_style("info", Style("blue"))
        formatter.set_style("comment", Style("green"))
        formatter.set_style("warning", Style("yellow"))
        formatter.set_style("debug", Style("default", options=["dark"]))
        formatter.set_style("success", Style("green"))

        # Dark variants
        formatter.set_style("c1_dark", Style("cyan", options=["dark"]))
        formatter.set_style("c2_dark", Style("default", options=["bold", "dark"]))
        formatter.set_style("success_dark", Style("green", options=["dark"]))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        # Fixme: 调试信息
        # io.set_verbosity(Verbosity.DEBUG)

        if io.is_debug():
            io.write_line(
                "----------------------- create_io done! -----------------------"
            )

        self._io = io

        return io

    def render_error(self, error: Exception, io: IO) -> None:
        # We set the solution provider repository here to load providers
        # only when an error occurs
        print(
            "----------------------- render_error starting...  -----------------------"
        )
        self.set_solution_provider_repository(self._get_solution_provider_repository())

        super().render_error(error, io)

    def _run(self, io: IO) -> int:
        print("----------------------- _run starting...  -----------------------")
        self._disable_plugins = io.input.parameter_option("--no-plugins")
        self._disable_cache = io.input.has_parameter_option("--no-cache")

        # self._load_plugins(io)

        if io.is_debug():
            io.write_line(
                "-----------------------Debug super()._run(io) starting... -----------------------"
            )
        exit_code: int = super()._run(io)

        if io.is_debug():
            io.write_line(
                "-----------------------Debug super()._run(io) done! -----------------------"
            )

        print("----------------------- _run done...  -----------------------")
        return exit_code

    def _configure_io(self, io: IO) -> None:
        # We need to check if the command being run
        # is the "run" command.
        print(
            "----------------------- _configure_io init starting...  -----------------------"
        )
        definition = self.definition
        with suppress(CleoError):
            io.input.bind(definition)

        name = io.input.first_argument
        if name == "run":
            from openfund.console.io.inputs.run_argv_input import RunArgvInput

            input = cast("ArgvInput", io.input)
            run_input = RunArgvInput([self._name or "", *input._tokens])
            # For the run command reset the definition
            # with only the set options (i.e. the options given before the command)
            for option_name, value in input.options.items():
                if value:
                    option = definition.option(option_name)
                    run_input.add_parameter_option("--" + option.name)
                    if option.shortcut:
                        shortcuts = re.split(r"\|-?", option.shortcut.lstrip("-"))
                        shortcuts = [s for s in shortcuts if s]
                        for shortcut in shortcuts:
                            run_input.add_parameter_option("-" + shortcut.lstrip("-"))

            with suppress(CleoError):
                run_input.bind(definition)

            for option_name, value in input.options.items():
                if value:
                    run_input.set_option(option_name, value)

            io.set_input(run_input)

        super()._configure_io(io)

    def register_command_loggers(
        self, event: Event, event_name: str, _: EventDispatcher
    ) -> None:
        from openfund.console.clogs.filters import OPENFUND_FILTER
        from openfund.console.clogs.io_formatter import IOFormatter
        from openfund.console.clogs.io_handler import IOHandler

        from openfund.locations import log_file
        from openfund.console.clogs.file_handler import FileHandler
        from openfund.console.clogs.file_formatter import FileFormatter

        # print(
        #     "----------------------- register_command_loggers init starting...  -----------------------"
        # )
        assert isinstance(event, ConsoleCommandEvent)
        command = event.command
        if not isinstance(command, Command):
            return
        io = event.io

        loggers = [
            "openfund.packages.locker",
            "openfund.packages.package",
            "openfund.utils.password_manager",
        ]

        loggers += command.loggers

        handler = IOHandler(io)
        handler.setFormatter(IOFormatter())

        fileHandler = FileHandler(log_file(command.name))
        fileHandler.setFormatter(FileFormatter())

        level = logging.WARNING

        if io.is_debug():
            level = logging.DEBUG
        elif io.is_very_verbose() or io.is_verbose():
            level = logging.INFO

        logging.basicConfig(
            level=level,
            handlers=[handler, fileHandler],
        )

        # only log third-party packages when very verbose
        if not io.is_very_verbose():
            handler.addFilter(OPENFUND_FILTER)

        for name in loggers:
            logger = logging.getLogger(name)

            _level = level
            # The builders loggers are special and we can actually
            # start at the INFO level.
            if (
                logger.name.startswith("poetry.core.masonry.builders")
                and _level > logging.INFO
            ):
                _level = logging.INFO

            logger.setLevel(_level)

    def configure_env(self, event: Event, event_name: str, _: EventDispatcher) -> None:
        from openfund.console.commands.env_command import EnvCommand
        from openfund.console.commands.self.self_command import SelfCommand

        print(
            "----------------------- configure_env init starting...  -----------------------"
        )
        assert isinstance(event, ConsoleCommandEvent)
        command = event.command
        if not isinstance(command, EnvCommand) or isinstance(command, SelfCommand):
            return

        if command._env is not None:
            return

        from openfund.utils.env import EnvManager

        io = event.io
        openfund = command.openfund

        env_manager = EnvManager(openfund, io=io)
        env = env_manager.create_venv()

        if env.is_venv() and io.is_verbose():
            io.write_line(f"Using virtualenv: <comment>{env.path}</>")

        command.set_env(env)

    @classmethod
    def configure_installer_for_event(
        cls, event: Event, event_name: str, _: EventDispatcher
    ) -> None:
        from openfund.console.commands.installer_command import (
            InstallerCommand,
        )

        print(
            "----------------------- configure_installer_for_event starting...  -----------------------"
        )
        assert isinstance(event, ConsoleCommandEvent)
        command = event.command
        if not isinstance(command, InstallerCommand):
            return

        # If the command already has an installer
        # we skip this step
        if command._installer is not None:
            return

        cls.configure_installer_for_command(command, event.io)

    @staticmethod
    def configure_installer_for_command(command: InstallerCommand, io: IO) -> None:
        from openfund.installation.installer import Installer

        print(
            "----------------------- configure_installer_for_command starting...  -----------------------"
        )
        openfund = command.openfund
        installer = Installer(
            io,
            command.env,
            openfund.package,
            openfund.locker,
            openfund.pool,
            openfund.config,
            disable_cache=openfund.disable_cache,
        )
        command.set_installer(installer)

    def _load_plugins(self, io: IO | None = None) -> None:
        print(
            "----------------------- _load_plugins init starting...  -----------------------"
        )

        if self._plugins_loaded:
            return

        if io is None:
            io = NullIO()

        self._disable_plugins = io.input.has_parameter_option("--no-plugins")

        if not self._disable_plugins:
            from openfund.plugins.application_plugin import ApplicationPlugin
            from openfund.plugins.plugin_manager import PluginManager

            manager = PluginManager(ApplicationPlugin.group)
            manager.load_plugins()
            manager.activate(self)

            # We have to override the command from poetry-plugin-export
            # with the wrapper.
            if self.command_loader.has("export"):
                del self.command_loader._factories["export"]
            self.command_loader._factories["export"] = load_command("export")

        self._plugins_loaded = True

    @property
    def _default_definition(self) -> Definition:
        from cleo.io.inputs.option import Option

        print(
            "----------------------- _default_definition init starting...  -----------------------"
        )

        definition = super()._default_definition

        definition.add_option(
            Option("--no-plugins", flag=True, description="Disables plugins.")
        )

        definition.add_option(
            Option(
                "--no-cache", flag=True, description="Disables Poetry source caches."
            )
        )

        definition.add_option(
            Option(
                "--directory",
                "-C",
                flag=False,
                description=(
                    "The working directory for the Poetry command (defaults to the"
                    " current working directory)."
                ),
            )
        )

        return definition

    def _get_solution_provider_repository(self) -> SolutionProviderRepository:
        from crashtest.solution_providers.solution_provider_repository import (
            SolutionProviderRepository,
        )

        from openfund.mixology.solutions.providers.python_requirement_solution_provider import (
            PythonRequirementSolutionProvider,
        )

        repository = SolutionProviderRepository()
        repository.register_solution_providers([PythonRequirementSolutionProvider])

        return repository


def main() -> int:
    exit_code: int = Application().run()
    return exit_code


if __name__ == "__main__":
    main()
