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

"""Contains main window class of the application."""

import logging
from typing import Final

from ensure_dialog import EnsureSessionDialog
from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QWidget,
)
from qasync import asyncSlot
from settings_dialog import SettingsDialog
from telegram import fetch_all_dialogs

_LOGGER: Final = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window class of the application."""

    def __init__(self, parent=None) -> None:
        """Default constructor of the main window class of the application.

        Args:
            parent: Parent object instance.
        """
        _LOGGER.debug("MainWindow, constructor, begin")
        super().__init__(parent)

        self._main_setup()

        self._create_actions()
        self._create_start_menu()
        self._create_toolbar()

        self._create_dialogs_table()
        self._create_dialogs_fetch_button()
        self._create_layout()

        _LOGGER.debug("MainWindow, constructor, end")

    def _main_setup(self) -> None:
        """Performs the main setup of the application main window."""
        _LOGGER.debug("MainWindow, main setup, begin")
        self.setWindowTitle("Trollogeddon")
        self.setFixedSize(QSize(640, 480))
        _LOGGER.debug("MainWindow, main setup, end")

    def _create_actions(self) -> None:
        """Create menu actions of the application main window."""
        _LOGGER.debug("MainWindow, create actions, begin")
        self._settings_action = QAction("&Settings", self, triggered=self._settings_action_triggered)
        self._ensure_action = QAction("&Ensure Session", self, triggered=self._ensure_action_triggered)
        self._exit_action = QAction("E&xit", self, triggered=QApplication.instance().quit)
        _LOGGER.debug("MainWindow, create actions, end")

    def _create_start_menu(self) -> None:
        """Create start menu item of the menu bar."""
        _LOGGER.debug("MainWindow, create start menu, begin")
        start_menu = self.menuBar().addMenu("&Start")
        start_menu.addAction(self._settings_action)
        start_menu.addAction(self._ensure_action)
        start_menu.addSeparator()
        start_menu.addAction(self._exit_action)
        _LOGGER.debug("MainWindow, create start menu, end")

    def _create_toolbar(self) -> None:
        """Create main toolbar of the main window."""
        _LOGGER.debug("MainWindow, create toolbar, begin")
        toolbar = QToolBar("Main Toolbar")
        toolbar.addAction(self._settings_action)
        toolbar.addAction(self._ensure_action)
        toolbar.addSeparator()
        toolbar.addAction(self._exit_action)
        self.addToolBar(toolbar)
        _LOGGER.debug("MainWindow, create toolbar, end")

    def _create_dialogs_table(self) -> None:
        """Creates the dialogs table."""
        _LOGGER.debug("MainWindow, create dialogs table, begin")
        self._dialogs_table = QTableWidget(self)
        self._dialogs_table.setColumnCount(2)
        self._dialogs_table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Chat Name")))
        _LOGGER.debug("MainWindow, create dialogs table, end")

    def _create_dialogs_fetch_button(self) -> None:
        """Creates the button which fetches all the dialogs."""
        _LOGGER.debug("MainWindow, create fetch button, begin")
        self._fetch_button = QPushButton(self.tr("Fetch All Dialogs"), clicked=self._fetch_button_clicked)
        _LOGGER.debug("MainWindow, create fetch button, end")

    def _create_layout(self) -> None:
        """Create layout of the app main window."""
        _LOGGER.debug("MainWindow, create layout, begin")

        layout = QGridLayout(self)
        layout.setSpacing(10)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        layout.addWidget(self._dialogs_table, 0, 0)
        layout.addWidget(self._fetch_button, 1, 0)

        _LOGGER.debug("MainWindow, create layout, end")

    @Slot()
    def _settings_action_triggered(self) -> None:
        """Slot which handles the open settings action trigger signal."""
        _LOGGER.debug("MainWindow, settings action trigger, begin")
        SettingsDialog(self).exec()
        _LOGGER.debug("MainWindow, settings action trigger, begin")

    @Slot()
    def _ensure_action_triggered(self) -> None:
        """Slot which handles the ensure session action trigger signal."""
        _LOGGER.debug("MainWindow, ensure action trigger, begin")
        EnsureSessionDialog(self).exec()
        _LOGGER.debug("MainWindow, ensure action trigger, end")

    @asyncSlot()
    async def _fetch_button_clicked(self):
        """Async slot which handles the fetch all the dialogs button click signal."""
        _LOGGER.debug("MainWindow, fetch button click, begin")

        self._dialogs_table.clearContents()
        dialogs = await fetch_all_dialogs()

        self._dialogs_table.setRowCount(len(dialogs))
        for index, dialog in enumerate(dialogs):
            self._dialogs_table.setItem(index, 0, QTableWidgetItem(dialog.name))

        _LOGGER.debug("MainWindow, fetch button click, end")
