import sys

from ui.App import App

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())