# Python Qt5 application
Python Qt5 GUI app with pyinstaller

See: [LICENSE](LICENSE)

## About
Quick poc app that uses PyInstaller to create a self-contained onefile app.
It monitors ~/repos/my_repo in the background and lists the current branches with a manual UI refresh button.

## Notes
* https://doc.qt.io/qtforpython-6/deployment/deployment-pyinstaller.html At the time of writing, Qt6 does not work with pyinstaller `--onefile`.
* The pyqt5-tools package has version compatibility issues and won't launch the designer.
