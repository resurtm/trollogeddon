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


from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton
from qasync import asyncSlot, QApplication

from settings_dialog import SettingsDialog
from telegram import create_client


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Trollogeddon")
        self.setFixedSize(QSize(640, 480))

        connect_button = QPushButton("Connect Now", clicked=self._connect_clicked)
        self.setCentralWidget(connect_button)

        settings_action = QAction("&Settings", self, triggered=self._settings_action_triggered)
        exit_action = QAction("E&xit", self, triggered=QApplication.instance().quit)

        start_menu = self.menuBar().addMenu("&Start")
        start_menu.addAction(settings_action)
        start_menu.addAction(exit_action)

    @Slot()
    def _settings_action_triggered(self) -> None:
        SettingsDialog().exec()

    @asyncSlot()
    async def _connect_clicked(self):
        await create_client()
