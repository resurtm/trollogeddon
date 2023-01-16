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

"""Telegram API and related routines."""

import logging
from typing import Final
from typing import Optional

from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError

from settings import AppSettings

SESSION_NAME: Final = "trollogeddon"

_LOGGER: Final = logging.getLogger(__name__)


async def send_otp_code(phone: str) -> str:
    _LOGGER.debug("Send OTP code, begin")
    client = _create_client()
    await client.connect()
    result = await client.send_code_request(phone=phone, force_sms=True)
    _LOGGER.debug("Send OTP code, end")
    return result.phone_code_hash


async def verify_otp_code(phone: str, otp_code: str, phone_hash: str, password: Optional[str] = None) -> None:
    _LOGGER.debug("Verify OTP code, begin")
    client = _create_client()
    await client.connect()
    try:
        await client.sign_in(phone=phone, code=otp_code, phone_code_hash=phone_hash)
    except SessionPasswordNeededError:
        await client.sign_in(phone=phone, code=otp_code, phone_code_hash=phone_hash, password=password)
    print(await client.get_me())
    _LOGGER.debug("Verify OTP code, end")


def _create_client() -> TelegramClient:
    _LOGGER.debug("Create client, begin")
    settings = AppSettings()
    client = TelegramClient(SESSION_NAME, int(settings.api_id()), settings.api_hash())
    _LOGGER.debug("Create client, end")
    return client
