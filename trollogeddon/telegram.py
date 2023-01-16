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
from typing import Final, List, Optional

from settings import AppSettings
from telethon import TelegramClient  # type: ignore
from telethon.errors.rpcerrorlist import SessionPasswordNeededError  # type: ignore
from telethon.tl.custom.dialog import Dialog  # type: ignore

SESSION_NAME: Final = "trollogeddon"

_LOGGER: Final = logging.getLogger(__name__)


async def fetch_all_dialogs() -> List[Dialog]:
    """Fetch all the chats and dialogs of the user.

    Returns:
        List with all the chats and dialogs of the user.
    """
    client = _create_client()
    await client.connect()

    dialogs = await client.get_dialogs()
    await client.disconnect()

    return dialogs


async def send_otp_code(phone: str) -> Optional[str]:
    """Request a one time used OTP code to be sent to the user.

    Returns:
        The resulting phone code cash which was returned by the Telegram API.
        None value is returned in case the user was already authorized (i.e. there's no need in OTP code).
    """
    _LOGGER.debug("Send OTP code, begin")

    client = _create_client()
    await client.connect()

    if await client.is_user_authorized():
        await client.disconnect()
        _LOGGER.debug("Send OTP code, already authorized, end")
        return None

    result = await client.send_code_request(phone=phone, force_sms=True)
    await client.disconnect()

    _LOGGER.debug("Send OTP code, code requested, end")
    return result.phone_code_hash


async def verify_otp_code(phone: str, otp_code: str, phone_hash: str, password: Optional[str] = None) -> None:
    """Verify the OTP code which was received by the user after requesting it.

    Args:
         phone: phone number (e.g. "+49 175 ...").
         otp_code: the OTP code to be verified.
         phone_hash: phone hash which was returned in the Telegram API response.
         password: user's cloud password. Don't provide it or use the `None` value if it's not used by the user.
    """
    _LOGGER.debug("Verify OTP code, begin")

    client = _create_client()
    await client.connect()

    if await client.is_user_authorized():
        await client.disconnect()
        _LOGGER.debug("Verify OTP code, already authorized, end")
        return

    try:
        _LOGGER.debug("Verify OTP code, sign in")
        await client.sign_in(phone=phone, code=otp_code, phone_code_hash=phone_hash)
    except SessionPasswordNeededError:
        _LOGGER.debug("Verify OTP code, caught SessionPasswordNeededError")
        await client.sign_in(password=password)
    finally:
        await client.disconnect()

    _LOGGER.debug("Verify OTP code, end")


def _create_client() -> TelegramClient:
    _LOGGER.debug("Create client, begin")

    settings = AppSettings()
    client = TelegramClient(SESSION_NAME, int(settings.api_id()), settings.api_hash())

    _LOGGER.debug("Create client, end")
    return client
