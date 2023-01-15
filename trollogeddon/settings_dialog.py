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

"""Application UI settings related code."""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

from settings import AppSettings


class SettingsDialog(QDialog):
    """Application UI settings dialog class."""

    def __init__(self, parent=None) -> None:
        """Default constructor of the settings dialog class.

        Args:
            parent: parent object.
        """
        super().__init__(parent)

        self.setWindowTitle(self.tr("Application Settings"))

        self._prepare_settings()
        self._create_api_id_controls()
        self._create_api_hash_controls()
        self._create_save_button()
        self._create_layout()

    def _prepare_settings(self) -> None:
        """Prepare application settings."""
        self._settings = AppSettings()

    def _create_api_id_controls(self) -> None:
        """Create input & label PySide controls to be used with the Telegram App API_ID value."""
        self._api_id_input = QLineEdit()
        self._api_id_input.setText(self._settings.api_id())

        self._api_id_label = QLabel(self.tr("App api_id:"))
        self._api_id_label.setBuddy(self._api_id_input)

    def _create_api_hash_controls(self) -> None:
        """Create input & label PySide controls to be used with the Telegram App APP_HASH value."""
        self._api_hash_input = QLineEdit()
        self._api_hash_input.setText(self._settings.api_hash())

        self._api_hash_label = QLabel(self.tr("App api_hash:"))
        self._api_hash_label.setBuddy(self._api_hash_input)

    def _create_save_button(self) -> None:
        """Prepare application settings save button."""
        self._save_button = QPushButton(self.tr("Save"), clicked=self._save_button_clicked)

    @Slot()
    def _save_button_clicked(self) -> None:
        """Slot method which handles the application settings save button signal."""
        self._settings.set_api_id(self._api_id_input.text())
        self._settings.set_api_hash(self._api_hash_input.text())
        self.close()

    def _create_layout(self) -> None:
        """Creates a layout of the settings dialog."""
        layout = QGridLayout(self)

        layout.addWidget(self._api_id_label, 0, 0)
        layout.addWidget(self._api_id_input, 0, 1)

        layout.addWidget(self._api_hash_label, 1, 0)
        layout.addWidget(self._api_hash_input, 1, 1)

        layout.addWidget(self._save_button, 2, 0, 1, 2)
