# browser.py

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class ReaderBrowser(QWebEngineView):
    def __init__(self):
        super().__init__()

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

    def load_local_html(self, path: str):
        """Load a local HTML file from disk."""
        from PyQt5.QtCore import QUrl
        self.load(QUrl.fromLocalFile(path))

    def set_zoom(self, factor: float):
        self.setZoomFactor(factor)
