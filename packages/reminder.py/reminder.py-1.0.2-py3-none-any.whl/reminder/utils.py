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

from typing import TYPE_CHECKING
import logging
import uuid

if TYPE_CHECKING:
    from typing import Optional

__all__ = ('setup_logging', 'generate_schedule_id')

def setup_logging(*,
                  handler: Optional[logging.Handler] = None,
                  level: Optional[int] = None,
                  root: bool = True) -> None:
    """
    Setup logging configuration.
    """
    if level is None:
        level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler()

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname}] {name}: {message}', dt_fmt, style='{')

    if root:
        logger = logging.getLogger()
    else:
        library, _, _ = __name__.partition('.')
        logger = logging.getLogger(library)

    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


def generate_schedule_id(existing_ids: list[str]) -> str:
    """
    Generate a unique schedule ID that does not conflict with existing IDs.

    Parameters
    ----------
    existing_ids: list[str]
        A list of IDs that already exist.

    Returns
    -------
    str
        A unique ID not present in existing_ids.
    """
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id