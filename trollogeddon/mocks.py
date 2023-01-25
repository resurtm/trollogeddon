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

"""Mocked data for testing and development purposes."""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, call

from telethon.tl.custom.dialog import Dialog  # type: ignore
from telethon.tl.custom.message import Message  # type: ignore


@dataclass
class MockedDialog(Dialog):
    """Mocked Telegram dialog dataclass for testing purposes."""

    name: str


@dataclass
class MockedMessage(Message):
    """Mocked Telegram message dataclass for testing purposes."""

    id: int
    delete: AsyncMock


def get_mocked_dialog1() -> Dialog:
    """Create a mocked dialog instance, variation 1.

    Returns:
        New mocked dialog instance, variation 1.
    """
    return MockedDialog(name="Chat 111")


def get_mocked_dialog2() -> Dialog:
    """Create a mocked dialog instance, variation 2.

    Returns:
        New mocked dialog instance, variation 2.
    """
    return MockedDialog(name="Chat 222")


def get_mocked_message1() -> MockedMessage:
    """Create a mocked message instance, variation 1.

    Returns:
        New mocked message instance, variation 1.
    """
    return MockedMessage(id=123123, delete=AsyncMock())


def get_mocked_message2() -> MockedMessage:
    """Create a mocked message instance, variation 2.

    Returns:
        New mocked message instance, variation 2.
    """
    return MockedMessage(id=111999, delete=AsyncMock())
