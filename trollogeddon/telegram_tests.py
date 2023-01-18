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

"""Telegram API and related routines. Tests."""

import logging
from typing import Final
from unittest.mock import AsyncMock

import pytest
from mocks import get_mocked_dialog1, get_mocked_dialog2
from pytest_mock.plugin import MockerFixture
from telegram import fetch_all_dialogs
from telethon.tl.custom.dialog import Dialog  # type: ignore

# Local logger instance for the current file.
_LOGGER: Final = logging.getLogger(__name__)

# Mocked dialogs list for testing purposes.
_DIALOGS: Final = [get_mocked_dialog1(), get_mocked_dialog2()]


@pytest.mark.asyncio
async def test_fetch_all_dialogs(mocker: MockerFixture) -> None:
    """Test the `fetch_all_dialogs` function.

    Args:
        mocker: Mocker fixture instance to mock the things.
    """
    con_mock = mocker.patch("telegram.TelegramClient.connect", side_effect=AsyncMock())
    dial_mock = mocker.patch("telegram.TelegramClient.get_dialogs", side_effect=AsyncMock(return_value=_DIALOGS))
    disc_mock = mocker.patch("telegram.TelegramClient.disconnect", side_effect=AsyncMock())

    dialogs = await fetch_all_dialogs()  # actual tested function call
    assert con_mock.call_count == 1
    assert dial_mock.call_count == 1
    assert disc_mock.call_count == 1
    assert dialogs == _DIALOGS
