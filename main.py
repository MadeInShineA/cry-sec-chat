import sys
import traceback

from ui.App import App


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    try:
        sys.excepthook = except_hook
        app = App(sys.argv)
        sys.exit(app.exec())
    except Exception as e:
        print(e)
        sys.exit(traceback.format_exc())
