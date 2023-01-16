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

from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from qasync import asyncSlot

from telegram import send_otp_code, verify_otp_code


class EnsureSessionDialog(QDialog):
    """Ensure user session ensure dialog class."""

    def __init__(self, parent=None) -> None:
        """Default constructor of the user session ensure dialog class.

        Args:
            parent: parent object.
        """
        super().__init__(parent)

        self._create_phone_controls()
        self._create_otp_controls()
        self._create_password_controls()
        self._create_action_buttons()
        self._create_layout()

    def _create_phone_controls(self) -> None:
        self._phone_input = QLineEdit(self)
        self._phone_label = QLabel(self.tr("Phone Number:"))
        self._phone_label.setBuddy(self._phone_input)

    def _create_otp_controls(self) -> None:
        self._otp_input = QLineEdit(self)
        self._otp_label = QLabel(self.tr("OTP Code:"))
        self._otp_label.setBuddy(self._otp_input)

    def _create_password_controls(self) -> None:
        self._password_input = QLineEdit(self)
        self._password_label = QLabel(self.tr("Password:"))
        self._password_label.setBuddy(self._password_input)

    def _create_action_buttons(self) -> None:
        """Prepare the user session ensure action buttons."""
        self._send_otp = QPushButton(self.tr("Send OTP"), clicked=self._send_otp_clicked)
        self._sign_in = QPushButton(self.tr("Sign In"), clicked=self._sign_in_clicked)

    def _create_layout(self) -> None:
        """Creates a layout of the user session ensure dialog."""
        layout = QGridLayout(self)
        layout.setSpacing(10)
        self.setLayout(layout)

        layout.addWidget(self._phone_label, 0, 0)
        layout.addWidget(self._phone_input, 0, 1)

        layout.addWidget(self._otp_label, 1, 0)
        layout.addWidget(self._otp_input, 1, 1)

        layout.addWidget(self._password_label, 2, 0)
        layout.addWidget(self._password_input, 2, 1)

        layout.addWidget(self._send_otp, 3, 0)
        layout.addWidget(self._sign_in, 3, 1)

    @asyncSlot()
    async def _send_otp_clicked(self) -> None:
        self._phone_hash = await send_otp_code(phone=self._phone_input.text())

    @asyncSlot()
    async def _sign_in_clicked(self) -> None:
        await verify_otp_code(
            phone=self._phone_input.text(),
            otp_code=self._otp_input.text(),
            phone_hash=self._phone_hash,
            password=self._password_input.text(),
        )
