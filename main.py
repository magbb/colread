# main.py

import sys
import argparse
from PyQt5.QtWidgets import QApplication

from window import ReaderWindow
import config
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ColRead: Column-based document reader for QT")
    parser.add_argument("--cols", type=int, default=config.DEFAULT_COLUMNS)
    args = parser.parse_args()

    app = QApplication(sys.argv)

    # Find HTML path
    base = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base, "resources", "template.html")

    window = ReaderWindow(html_path=html_path, columns=args.cols)
    window.show()

    sys.exit(app.exec_())
