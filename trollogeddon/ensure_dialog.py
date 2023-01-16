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

"""File contains class with the user session ensure dialog things."""

import logging
from typing import Final, Optional

from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton
from qasync import asyncSlot  # type: ignore
from telegram import send_otp_code, verify_otp_code

_LOGGER: Final = logging.getLogger(__name__)


class EnsureSessionDialog(QDialog):
    """Ensure user session ensure dialog class."""

    _phone_input: QLineEdit
    _phone_label: QLabel

    _otp_input: QLineEdit
    _otp_label: QLabel

    _password_input: QLineEdit
    _password_label: QLabel

    _send_otp_button: QPushButton
    _sign_in_button: QPushButton

    _phone_hash: Optional[str]

    def __init__(self, parent=None) -> None:
        """Construct a new instance of the user session ensure dialog class.

        Args:
            parent: parent object.
        """
        _LOGGER.debug("EnsureSessionDialog, constructor, begin")
        super().__init__(parent)

        self._create_phone_controls()
        self._create_otp_controls()
        self._create_password_controls()
        self._create_action_buttons()
        self._create_layout()

        _LOGGER.debug("EnsureSessionDialog, constructor, end")

    def _create_phone_controls(self) -> None:
        """Create phone number input related controls."""
        _LOGGER.debug("EnsureSessionDialog, create phone controls, begin")

        self._phone_input = QLineEdit(self)
        self._phone_label = QLabel("Phone Number:")
        self._phone_label.setBuddy(self._phone_input)

        _LOGGER.debug("EnsureSessionDialog, create phone controls, end")

    def _create_otp_controls(self) -> None:
        """Create OTP code input related controls."""
        _LOGGER.debug("EnsureSessionDialog, create OTP controls, begin")

        self._otp_input = QLineEdit(self)
        self._otp_label = QLabel("OTP Code:")
        self._otp_label.setBuddy(self._otp_input)

        _LOGGER.debug("EnsureSessionDialog, create OTP controls, end")

    def _create_password_controls(self) -> None:
        """Create cloud password input related controls."""
        _LOGGER.debug("EnsureSessionDialog, create password controls, begin")

        self._password_input = QLineEdit(self)
        self._password_label = QLabel("Password:")
        self._password_label.setBuddy(self._password_input)

        _LOGGER.debug("EnsureSessionDialog, create password controls, end")

    def _create_action_buttons(self) -> None:
        """Prepare the user session ensure action buttons."""
        _LOGGER.debug("EnsureSessionDialog, create action buttons, begin")

        self._send_otp_button = QPushButton("Send OTP")
        self._send_otp_button.clicked.connect(self._send_otp_clicked)  # type: ignore
        self._sign_in_button = QPushButton("Sign In")
        self._sign_in_button.clicked.connect(self._sign_in_clicked)  # type: ignore

        _LOGGER.debug("EnsureSessionDialog, create action buttons, end")

    def _create_layout(self) -> None:
        """Create a layout of the user session ensure dialog."""
        _LOGGER.debug("EnsureSessionDialog, create layout, begin")

        layout = QGridLayout(self)
        layout.setSpacing(10)
        self.setLayout(layout)

        layout.addWidget(self._phone_label, 0, 0)
        layout.addWidget(self._phone_input, 0, 1)

        layout.addWidget(self._otp_label, 1, 0)
        layout.addWidget(self._otp_input, 1, 1)

        layout.addWidget(self._password_label, 2, 0)
        layout.addWidget(self._password_input, 2, 1)

        layout.addWidget(self._send_otp_button, 3, 0)
        layout.addWidget(self._sign_in_button, 3, 1)

        _LOGGER.debug("EnsureSessionDialog, create layout, end")

    @asyncSlot()
    async def _send_otp_clicked(self) -> None:
        """Qt slot handles the OTP code send button click signal."""
        _LOGGER.debug("EnsureSessionDialog, send OTP button click, begin")
        self._phone_hash = await send_otp_code(phone=self._phone_input.text())
        _LOGGER.debug("EnsureSessionDialog, send OTP button click, end")

    @asyncSlot()
    async def _sign_in_clicked(self) -> None:
        """Qt slot handles the sign-in button click signal."""
        _LOGGER.debug("EnsureSessionDialog, sign in button click, begin")

        if self._phone_hash is None:
            _LOGGER.debug("EnsureSessionDialog, phone hash is empty, do nothing")
        else:
            await verify_otp_code(
                phone=self._phone_input.text(),
                otp_code=self._otp_input.text(),
                phone_hash=self._phone_hash,
                password=self._password_input.text(),
            )

        _LOGGER.debug("EnsureSessionDialog, sign in button click, end")
