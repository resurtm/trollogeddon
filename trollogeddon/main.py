# Copyright 2023 resurtm@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# https://opensource.org/licenses/MIT

"""Application main function."""

import functools
import logging
from asyncio import AbstractEventLoop, Future, get_event_loop
from typing import Final, Literal

from main_window import MainWindow
from PySide6.QtWidgets import QApplication

_LOGGER: Final = logging.getLogger(__name__)


async def main() -> Literal[True]:
    """Application main function.

    Returns:
        True value that the main function executed correctly.
    """
    _LOGGER.debug("Main function, begin")
    loop = get_event_loop()
    future: Future = Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(functools.partial(_close_future, future, loop))

    main_window = MainWindow()
    main_window.show()

    _LOGGER.debug("Main function, await future")
    await future
    _LOGGER.debug("Main function, end")
    return True


def _close_future(future: Future, loop: AbstractEventLoop) -> None:
    loop.call_later(10, future.cancel)
    future.cancel()
