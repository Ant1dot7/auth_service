from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from logic.commands.base import Command, CommandHandler, CommandResult
from logic.events.base import Event, EventHandler, EventResult
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(eq=False)
class Mediator:
    command_maps: dict[Command, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    event_maps: dict[Event, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[type[BaseQuery], QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_command(self, command: type[Command], command_handlers: Sequence[CommandHandler]):
        self.command_maps[command].extend(command_handlers)

    def register_event(self, event: type[Event], event_handlers: Sequence[EventHandler]):
        self.event_maps[event].extend(event_handlers)

    def register_query(self, query: type[BaseQuery], query_handler: QueryHandler):
        self.queries_map[query] = query_handler

    async def handle_command(self, command: Command) -> list[CommandResult]:
        command_type = command.__class__
        results = []
        for handler in self.command_maps[command_type]:
            results.append(await handler.handle(command))
        return results

    async def handle_events(self, events: list[Event]) -> list[EventResult]:
        results = []
        for event in events:
            event_type = event.__class__
            for handler in self.event_maps[event_type]:
                results.append(await handler.handle(event))
        return results

    async def handle_query(self, query: BaseQuery) -> Any:
        return await self.queries_map[query.__class__].handle(query=query)
