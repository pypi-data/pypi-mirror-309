"""
reminder.py

An async schedule reminders with custom event triggers on due time

:copyright: (c) 2024-present Snifo
:license: MIT, see LICENSE for more details.
"""

__title__ = 'reminder.py'
__version__ = '1.0.2'
__license__ = 'MIT License'
__author__ = 'Snifo'
__email__ = 'Snifo@mail.com'
__github__ = 'https://github.com/mrsnifo/reminder.py'


from .remind import Reminder
from .schedule import Schedule
from .utils import *