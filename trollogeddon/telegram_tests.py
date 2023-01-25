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
from typing import Final, Tuple
from unittest.mock import AsyncMock, MagicMock, call

import pytest
from mocks import (
    get_mocked_dialog1,
    get_mocked_dialog2,
    get_mocked_message1,
    get_mocked_message2,
)
from pytest_mock.plugin import MockerFixture
from telegram import delete_messages, fetch_all_dialogs
from telethon.tl.custom.dialog import Dialog  # type: ignore

# Local logger instance for the current file.
_LOGGER: Final = logging.getLogger(__name__)

# Mocked dialogs list for testing purposes.
_DIALOGS: Final = [get_mocked_dialog1(), get_mocked_dialog2()]
# Mocked entity IDs list for testing purposes.
_ENTITY_IDS: Final = [123, 234, 345]


@pytest.mark.asyncio
async def test_fetch_all_dialogs(mocker: MockerFixture) -> None:
    """Test the `fetch_all_dialogs` function.

    Args:
        mocker: Mocker fixture instance to mock the things.
    """
    con_mock, disc_mock = _prepare_telegram_client(mocker)
    dial_mock = mocker.patch("telegram.TelegramClient.get_dialogs", side_effect=AsyncMock(return_value=_DIALOGS))
    id_mock = mocker.patch("telegram.AppSettings.api_id", return_value="123")
    hash_mock = mocker.patch("telegram.AppSettings.api_hash", return_value="456")

    actual_result = await fetch_all_dialogs()  # actual tested function call

    assert con_mock.call_count == 1
    assert disc_mock.call_count == 1
    assert dial_mock.call_count == 1
    assert id_mock.call_count == 1
    assert hash_mock.call_count == 1
    assert actual_result == _DIALOGS


@pytest.mark.asyncio
async def test_delete_messages(mocker: MockerFixture) -> None:
    """Test the `delete_messages` function.

    Args:
        mocker: Mocker fixture instance to mock the things.
    """
    con_mock, disc_mock = _prepare_telegram_client(mocker)
    msg1_mock = get_mocked_message1()
    msg2_mock = get_mocked_message2()
    iter_mock = mocker.patch(
        "telegram.TelegramClient.iter_messages", return_value=_AsyncIterator([msg1_mock, msg2_mock])
    )

    await delete_messages(_ENTITY_IDS)

    assert con_mock.call_count == 1
    assert con_mock.call_args_list == [call()]
    assert disc_mock.call_count == 1
    assert disc_mock.call_args_list == [call()]
    assert iter_mock.call_count == 3
    assert iter_mock.call_args_list == [call(entity=entity_id, from_user="me") for entity_id in _ENTITY_IDS]
    assert msg1_mock.delete.call_count == 1
    assert msg1_mock.delete.call_args_list == [call()]
    assert msg2_mock.delete.call_count == 1
    assert msg2_mock.delete.call_args_list == [call()]


def _prepare_telegram_client(mocker: MockerFixture) -> Tuple[MagicMock, MagicMock]:
    def ctor(session_name: str, api_id: str, api_hash: str) -> None:
        pass

    mocker.patch("telegram.TelegramClient.__init__", wraps=ctor)
    con_mock = mocker.patch("telegram.TelegramClient.connect", wraps=AsyncMock())
    disc_mock = mocker.patch("telegram.TelegramClient.disconnect", wraps=AsyncMock())
    return con_mock, disc_mock


class _AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
