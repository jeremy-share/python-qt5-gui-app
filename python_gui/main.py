import sys
import os
import asyncio

import git
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic


class Worker(QThread):
    branchesFetched = pyqtSignal(list)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_branches_periodically())

    async def fetch_branches_periodically(self):
        while True:
            branches = await self.fetch_branches()
            self.branchesFetched.emit(branches)
            await asyncio.sleep(10)  # sleep for 10 seconds

    async def fetch_branches(self):
        repo_path = os.path.expanduser("~/repos/my_repo")
        try:
            repo = git.Repo(repo_path)
            branches = repo.branches
            branch_names = [branch.name for branch in branches]
            return branch_names
        except Exception as e:
            print(f"Error fetching branches: {e}")
            return []

    def trigger_fetch(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_and_emit_branches())

    async def fetch_and_emit_branches(self):
        branches = await self.fetch_branches()
        self.branchesFetched.emit(branches)


def resource_path(relative_path: str) -> str:
    """ Get an absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('main_window.ui'), self)  # Load the UI file

        self.update_branches_button.clicked.connect(self.fetch_branches)
        self.worker = Worker()
        self.worker.branchesFetched.connect(self.update_branches)
        self.worker.start()

        # System tray icon
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = resource_path('icon.png')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            print(f"Icon not found at {icon_path}")

        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.activated.connect(self.icon_activated)

    def fetch_branches(self):
        self.worker.trigger_fetch()

    def update_branches(self, branches):
        self.branches_list.clear()
        self.branches_list.addItems(branches)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        # self.tray_icon.showMessage(
        #     "Running in the background",
        #     "The application is still running. Click the tray icon to show it again.",
        #     QSystemTrayIcon.Information,
        #     2000
        # )

    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
