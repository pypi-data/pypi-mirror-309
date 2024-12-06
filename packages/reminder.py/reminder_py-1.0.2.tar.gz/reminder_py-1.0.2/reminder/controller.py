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

from .utils import generate_schedule_id
from typing import TYPE_CHECKING
from .schedule import Schedule
from datetime import datetime
import asyncio

if TYPE_CHECKING:
    from typing import Callable, Any, List


import logging
_logger = logging.getLogger(__name__)

__all__ = ('Controller',)

class Controller:
    """
    The Controller class manages schedules and dispatches events.
    """
    __slots__ = ('schedules', '_cycle', '__dispatch')

    def __init__(self, cycle: int, *, dispatcher: Callable[..., Any]) -> None:
        self.schedules: List[Schedule] = []
        self._cycle: int = cycle
        self.__dispatch: Callable[..., Any] = dispatcher

    def clear(self) -> None:
        """Clear all events from the event list."""
        self.schedules.clear()

    async def initiate(self) -> None:
        """
        Continuously loops through and executes each event in the event list
        at a set cycle interval.
        """
        self.__dispatch('initiate')
        while True:
            for schedule in self.schedules:
                if schedule.ends_at < datetime.now():
                    _logger.debug('Schedule "%s" (ID: %s) has ended at %s.',
                                 schedule.title, schedule.id, schedule.ends_at)
                    # Execute each event and handle any exceptions
                    self.__dispatch('schedule', schedule)
                    if schedule.callback:
                        self.__dispatch(schedule.callback, schedule)
                    try:
                        self.remove(schedule.id)
                    except ValueError:
                        pass
            # Wait for the next cycle
            await asyncio.sleep(self._cycle / 60)

    async def wait_for(self, schedule_id: str, /) -> None:
        """
        Wait for a schedule to complete based on its ID.

        Parameters
        ----------
        schedule_id: str
            The unique ID of the schedule to wait for.

        Raises
        ------
        ValueError
            If no schedule with the given ID exists.
        """
        schedule = self.get_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError(f'Schedule with ID {schedule_id!r} not found.')

        time_to_wait = (schedule.ends_at - schedule.created_at).total_seconds()
        _logger.debug('Waiting for schedule with ID: %s, duration: %s seconds', schedule_id, time_to_wait)

        await asyncio.sleep(time_to_wait)
        _logger.debug('Schedule with ID: %s has completed.', schedule_id)

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
        for schedule in self.schedules:
            if schedule.id == schedule_id:
                return schedule
        raise ValueError(f'Schedule with ID {schedule_id!r} not found.')

    def add(self, **kwargs) -> Schedule:
        """
        Add a new schedule with unique ID.

        Parameters
        ----------
        **kwargs: dict
            Keyword arguments for initializing a `Schedule` object.

        Returns
        -------
        Schedule
            The created and added schedule instance.
        """
        # Generate a unique ID and create a new Schedule
        schedule_id = generate_schedule_id([s.id for s in self.schedules])
        schedule = Schedule(schedule_id, **kwargs)
        self.schedules.append(schedule)
        return schedule

    def remove(self, schedule_id: str, /) -> None:
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
        for schedule in self.schedules:
            if schedule.id == schedule_id:
                self.schedules.remove(schedule)
                _logger.debug('Removed schedule with ID: %s', schedule.id)
                return
        raise ValueError(f'Schedule with ID {schedule_id!r} not found.')

    def remove_by_title(self, title: str, /) -> None:
        """
        Remove a schedule by its title.

        Parameters
        ----------
        title: str
            The title of the schedule to remove.

        Raises
        ------
        ValueError
            If no schedule with the given title is found.
        """
        for schedule in self.schedules:
            if schedule.title == title:
                self.schedules.remove(schedule)
                _logger.debug('Removed schedule with ID: %s', schedule.id)
                return
        raise ValueError(f'Schedule with title {title!r} not found.')