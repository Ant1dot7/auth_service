from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Sequence

from logic.commands.base import Command, CommandHandler, CommandResult


@dataclass(eq=False)
class CommandMediator(ABC):
    command_maps: dict[Command, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    @abstractmethod
    def register_command(self, command: type[Command], command_handlers: Sequence[CommandHandler]):
        ...

    @abstractmethod
    async def handle_command(self, command: Command) -> CommandResult:
        ...


