"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from datetime import timedelta, datetime
from .controller import Controller
from typing import TYPE_CHECKING
from .utils import setup_logging
import asyncio

if TYPE_CHECKING:
    from typing import Callable, Any, Type, Self, List, Optional
    from .schedule import Schedule
    from types import TracebackType

import logging
_logger = logging.getLogger(__name__)

__all__ = ('Reminder',)

class Reminder:
    """
    A class to manage reminders.

    Parameters
    ----------
    cycle: int
        The cycle duration in milliseconds (default is 180ms). This determines
        how frequently the system checks for due schedules.
    loop: Optional[asyncio.AbstractEventLoop]
        The event loop to use, by default None (the current event loop is used).
    """

    def __init__(self, cycle: int = 180, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = loop
        self.controller: Controller = Controller(cycle, dispatcher=self.dispatch)

    async def __aenter__(self) -> Self:
        """
        Asynchronous context manager entry method.

        Returns
        -------
        Self
            The current instance of the client, allowing it to be used within an async context manager.
        """
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """
        Asynchronous context manager exit method.

        Parameters
        ----------
        exc_type: Optional[Type[BaseException]]
            The type of the exception raised, if any.
        exc_value: Optional[BaseException]
            The exception instance, if any.
        traceback: Optional[TracebackType]
            The traceback object, if any.
        """
        self.clear_schedules()

    async def _run_event(self, coro: Callable[..., Any], event_name: str, *args: Any, **kwargs: Any) -> None:
        # Run an event coroutine and handle exceptions.
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            await self.on_error(event_name, error, *args, **kwargs)

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        # Dispatch a specified event with a coroutine callback.
        method = 'on_' + event
        try:
            coro = getattr(self, method)
            if coro is not None and asyncio.iscoroutinefunction(coro):
                _logger.debug('Dispatching event %s', event)
                wrapped = self._run_event(coro, method, *args, **kwargs)
                # Schedule the task
                self.loop.create_task(wrapped, name=f'reminder:{method}')
        except AttributeError:
            pass
        except Exception as error:
            _logger.error('Event: %s Error: %s', event, error)

    def event(self, coro: Callable[..., Any], /) -> None:
        """
        Register a coroutine function as an event handler.

        This method assigns the given coroutine function to be used as an event handler with the same
        name as the coroutine function.

        Parameters
        ----------
        coro: Callable[..., Any]
            The coroutine function to register as an event handler.

        Example
        -------
        ```py
        @client.event
        async def on_initiate():
            ...
        ```
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The registered event must be a coroutine function')
        setattr(self, coro.__name__, coro)

    @staticmethod
    async def on_error(event_name: str, error: Exception, /, *args: Any, **kwargs: Any) -> None:
        """
        Handle errors occurring during event dispatch.

        This static method logs an exception that occurred during the processing of an event.

        Parameters
        ----------
        event_name: str
            The name of the event that caused the error.
        error: Exception
            The exception that was raised.
        *args: Any
            Positional arguments passed to the event.
        **kwargs: Any
            Keyword arguments passed to the event.
        """
        _logger.exception('Ignoring error: %s from %s, args: %s kwargs: %s', error, event_name,
                          args, kwargs)

    def initiate_event_loop(self) -> None:
        if self.loop is not None:
            return

        if self.loop is None:
            self.loop = asyncio.get_running_loop() # Type:  ignore


    async def wait_for(self, schedule: Schedule, /) -> None:
        """
        Wait for a schedule to complete based on its ID.

        Parameters
        ----------
        schedule: Schedule
            The schedule object to wait for.

        Raises
        ------
        ValueError
            If no schedule with the given ID exists.
        """
        await self.controller.wait_for(schedule.id)

    def clear_schedules(self) -> None:
        self.controller.clear()

    def get_schedule_by_id(self, schedule_id: str) -> Schedule:
        """
        Retrieve a schedule by its unique ID.

        Parameters
        ----------
        schedule_id: str
            The unique ID of the schedule to retrieve.

        Returns
        -------
        Schedule
            The schedule with the matching ID.

        Raises
        ------
        ValueError
            If no schedule with the given ID exists.
        """
        return self.controller.get_schedule_by_id(schedule_id)

    def get_schedules(self) -> List[Schedule]:
        """
        Retrieve all schedules.

        Returns
        -------
        List[Schedule]
            A list of all schedules.
        """
        return self.controller.schedules

    def remove_schedule(self, schedule_id: str, /) -> None:
        """
        Remove a schedule by its unique ID.

        Parameters
        ----------
        schedule_id: str
            The unique ID of the schedule to remove.

        Raises
        ------
        ValueError
            If no schedule with the given ID is found.
        """
        self.controller.remove(schedule_id)

    def remove_schedule_by_title(self, title: str, /) -> None:
        """
        Remove a schedule by its title via the manager.

        Parameters
        ----------
        title: str
            The title of the schedule to remove.

        Raises
        ------
        ValueError
            If no schedule with the given title is found.
        """
        self.controller.remove_by_title(title)

    def add_schedule(self,
            title: Optional[str] = None,
            duration: timedelta = timedelta(seconds=0),
            description: Optional[str] = None,
            callback: Optional[str] = None) -> Schedule:
        """
        Add a new reminder with a specified title, duration, and optional description.

        Parameters
        ----------
        title: Optional[str]
            The title of the schedule.
        duration: timedelta
            The duration of the schedule.
        description: Optional[str]
            A description of the schedule.
        callback: Optional[Callable]
            A callback event name to be executed when the schedule ends.
        """
        if duration.total_seconds() <= 0:
            raise ValueError('Duration must be greater than zero.')

        reminder = {
            'title': title or 'No Title',
            'duration': duration,
            'created_at': datetime.now(),
            'description': description,
            'callback': callback
        }
        schedule = self.controller.add(**reminder)
        _logger.debug('Added reminder: %s', reminder)
        return schedule

    async def start(self):
        """
        Start the reminder system by initiating the event loop and controller.
        """
        self.initiate_event_loop()
        await self.controller.initiate()

    def run(self,
            log_handler: Optional[logging.Handler] = None,
            log_level: Optional[int] = None,
            root_logger: bool = False) -> None:
        """
        Run the reminder system, setting up logging and starting the asynchronous
        event loop.

        This method sets up the logging configuration and starts an asynchronous
        loop to run the main process, including the event handler and scheduler.

        Parameters
        ----------
        log_handler: Optional[logging.Handler]
            A logging handler to manage log outputs. If None, default logging
            handler will be used. (default is None)
        log_level: Optional[int]
            The log level to use for logging output. If None, the default level
            will be used. (default is None)
        root_logger: bool
            Whether to set up the root logger. (default is False)
        """
        if log_handler is None:
            setup_logging(handler=log_handler, level=log_level, root=root_logger)

        async def runner() -> None:
            async with self:
                await self.start()

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return
