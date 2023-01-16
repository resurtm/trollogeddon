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

"""File contains settings related things and utilities."""

import logging
from typing import Final

from PySide6.QtCore import QSettings

_SETTINGS_ORG_NAME: Final = "resurtm"
_SETTINGS_APP_NAME: Final = "trollogeddon"

_SETTINGS_TG_API_ID_KEY: Final = "telegram/api_id"
_SETTINGS_TG_API_HASH_KEY: Final = "telegram/api_hash"

_LOGGER: Final = logging.getLogger(__name__)


class AppSettings:
    """Class responsible for application settings routines."""

    def __init__(self) -> None:
        """Construct a new instance of the application settings class."""
        _LOGGER.debug("AppSettings, constructor, begin")
        self._settings = QSettings(_SETTINGS_ORG_NAME, _SETTINGS_APP_NAME)
        _LOGGER.debug("AppSettings, constructor, end")

    def api_id(self) -> str:
        """Get the existing current Telegram App API_ID value.

        Returns:
            The current Telegram App API_ID value.
        """
        _LOGGER.debug("AppSettings, get api ID")
        return str(self._settings.value(_SETTINGS_TG_API_ID_KEY))

    def set_api_id(self, api_id: str) -> None:
        """Set the new value of the Telegram App API_ID.

        Args:
            api_id: the new value to be used.
        """
        _LOGGER.debug("AppSettings, set api ID")
        self._settings.set_value(_SETTINGS_TG_API_ID_KEY, api_id)

    def api_hash(self) -> str:
        """Get the existing current Telegram App API_HASH value.

        Returns:
            The current Telegram App API_HASH value.
        """
        _LOGGER.debug("AppSettings, get api hash")
        return str(self._settings.value(_SETTINGS_TG_API_HASH_KEY))

    def set_api_hash(self, api_hash: str) -> None:
        """Set the new value of the Telegram App API_HASH.

        Args:
            api_hash: the new value to be used.
        """
        _LOGGER.debug("AppSettings, set api hash")
        self._settings.set_value(_SETTINGS_TG_API_HASH_KEY, api_hash)
