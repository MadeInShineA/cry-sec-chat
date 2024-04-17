import sys
import traceback

from ui.App import App

if __name__ == '__main__':

    try:
        app = App(sys.argv)
        sys.exit(app.exec())
    except Exception as e:
        print(e)
        sys.exit(traceback.format_exc())
