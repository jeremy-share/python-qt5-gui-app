pip-lock:
	pipenv lock

pip-install:
	pipenv install --dev

pip-update:
	pipenv update --dev

shell:
	pipenv shell

run:
	(cd python_gui && python3 main.py)

#designer:
#	pyqt5-tools designer

build-bin:
	pyinstaller --onefile --noconfirm --add-data "python_gui/icon.png:." --add-data "python_gui/main_window.ui:." --name python_async_gui  python_gui/main.py

#convert-ui:
#	(cd python_gui && pyuic6 -x main.ui -o main-ui.py)
