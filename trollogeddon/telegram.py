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
from typing import Collection, Final, List, Optional

from settings import AppSettings
from telethon import TelegramClient  # type: ignore
from telethon.errors.rpcerrorlist import SessionPasswordNeededError  # type: ignore
from telethon.tl.custom.dialog import Dialog  # type: ignore
from telethon.tl.custom.message import Message  # type: ignore

# Local logger instance for the current file.
_LOGGER: Final = logging.getLogger(__name__)

_SESSION_NAME: Final = "trollogeddon"
_FROM_USER: Final = "me"


async def fetch_all_dialogs() -> List[Dialog]:
    """Fetch all the chats and dialogs of the user.

    Returns:
        List with all the chats and dialogs of the user.
    """
    _LOGGER.debug("Fetch all dialogs, begin")

    client = _create_client()
    await client.connect()

    dialogs = await client.get_dialogs()
    await client.disconnect()

    _LOGGER.debug("Fetch all dialogs, end")
    return dialogs


async def delete_messages(entity_ids: Collection[int]) -> None:
    """Delete Telegram messages from the provided entity IDs.

    Args:
        entity_ids: Collection with entity IDs to be used to delete the messages from.
    """
    _LOGGER.debug("Delete messages, all, begin")

    client = _create_client()
    await client.connect()

    try:
        await _delete_messages_internal(entity_ids=entity_ids, client=client)
    finally:
        await client.disconnect()

    _LOGGER.debug("Delete messages, all, end")


async def _delete_messages_internal(entity_ids: Collection[int], client: TelegramClient) -> None:
    """Delete Telegram messages from the provided entity IDs. Internal implementation.

    Args:
        entity_ids: Collection with entity IDs to be used to delete the messages from.
        client: Telegram client which is already connected to be used to delete the messages.
    """
    _LOGGER.debug("Delete messages, all internal, begin")
    for entity_id in entity_ids:
        _LOGGER.debug("Delete messages, %d, begin", entity_id)

        message: Message
        async for message in client.iter_messages(entity=entity_id, from_user=_FROM_USER):
            _LOGGER.debug("Delete message, %d, %s, begin", entity_id, message.id)
            await message.delete()
            _LOGGER.debug("Delete message, %d, %s, end", entity_id, message.id)

        _LOGGER.debug("Delete messages, %d, end", entity_id)
    _LOGGER.debug("Delete messages, all internal, end")


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
    client = TelegramClient(_SESSION_NAME, int(settings.api_id()), settings.api_hash())

    _LOGGER.debug("Create client, end")
    return client
