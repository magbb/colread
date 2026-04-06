# window.py

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from browser import ReaderBrowser
import config


class ReaderWindow(QWidget):
    def __init__(self, html_path, columns=config.DEFAULT_COLUMNS):
        super().__init__()

        self.columns = columns
        self.zoom = 1.0

        self.setWindowTitle(f"ColRead")
        self.resize(1500, 1100)

        # Browser
        self.browser = ReaderBrowser()
        self.browser.load_local_html(html_path)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        self.setLayout(layout)

        # apply column count
        self.apply_column_js()

        # Shortcuts
        self.init_shortcuts()

    # ----------------------
    # JS injection
    # ----------------------
    def apply_column_js(self):
        script = f"""
            document.documentElement.style.setProperty('--columns', {self.columns});
            document.documentElement.style.setProperty('--fontSize', '{config.DEFAULT_FONT_SIZE}px');
            document.documentElement.style.setProperty('--fontFamily', "{config.DEFAULT_FONT_FAMILY}");
        """
        self.browser.page().runJavaScript(script)

    # ----------------------
    # Wheel handling
    # ----------------------
    def wheelEvent(self, event):
        # Zoom mode
        if event.modifiers() == Qt.ControlModifier:
            delta = config.ZOOM_STEP if event.angleDelta().y() > 0 else -config.ZOOM_STEP
            self.zoom = max(config.ZOOM_MIN, min(config.ZOOM_MAX, self.zoom + delta))
            self.browser.set_zoom(self.zoom)
            return

        # Normal scroll
        self.browser.page().runJavaScript(
            f"window.scrollBy({event.angleDelta().y() * config.SCROLL_SPEED}, 0);"
        )

    # ----------------------
    # Keyboard shortcuts
    # ----------------------
    def init_shortcuts(self):
        # Page left/right
        self.add_shortcut("Left", lambda: self.scroll_side(-800))
        self.add_shortcut("Right", lambda: self.scroll_side(800))

        # Home/end navigation
        self.add_shortcut("Ctrl+Home", lambda: self.scroll_to(0))
        self.add_shortcut("Ctrl+End", lambda: self.scroll_to("document.body.scrollWidth"))

        # Zoom reset
        self.add_shortcut("Ctrl+0", self.reset_zoom)

    def add_shortcut(self, seq, func):
        from PyQt5.QtWidgets import QShortcut
        QShortcut(QKeySequence(seq), self, func)

    # JS helpers
    def scroll_side(self, amount):
        self.browser.page().runJavaScript(f"window.scrollBy({amount}, 0);")

    def scroll_to(self, x):
        self.browser.page().runJavaScript(f"window.scrollTo({x}, 0);")

    def reset_zoom(self):
        self.zoom = 1.0
        self.browser.set_zoom(1.0)
