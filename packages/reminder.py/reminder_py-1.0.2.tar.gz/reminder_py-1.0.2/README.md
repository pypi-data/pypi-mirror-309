# reminder.py

[![PyPI - Version](https://img.shields.io/pypi/v/reminder.py?color=teal)](https://pypi.org/project/reminder.py)
[![Python Versions](https://img.shields.io/pypi/pyversions/reminder.py?color=teal)](https://pypi.org/project/reminder.py)

A Python library to manage scheduled reminders, events, and callbacks, designed for asynchronous operations.

## Installation

To install **reminder.py**, use the appropriate command for your operating system:

For Windows:

```bash
py -3 -m pip install --upgrade reminder.py
```

For macOS/Linux:

```bash
python3 -m pip install --upgrade reminder.py
```

## Quick Start

Here’s a simple example to get you started with reminder.py:

```python
from reminder import Reminder, Schedule
from datetime import timedelta

reminder = Reminder()

reminder.add_schedule('Task 1: Timer for 1 minute', timedelta(minutes=1))
reminder.add_schedule('Task 2: Reminder in 30 seconds', timedelta(seconds=30), callback='task_reminder')
reminder.add_schedule('Task 3: Another reminder in 30 seconds', timedelta(seconds=30), callback='task_reminder')

@reminder.event
async def on_initiate():
    print(f"Reminder has been initiated")
    
@reminder.event
async def on_schedule(schedule: Schedule):
    print(f"Triggered schedule: {schedule.title}")

@reminder.event
async def on_task_reminder(schedule: Schedule):
    print(f"Custom reminder callback triggered for schedule: {schedule.title}")

reminder.run()

```



## Documentation

For more detailed instructions,
visit the [reminder.py Documentation](https://reminderpy.readthedocs.io/latest/).
