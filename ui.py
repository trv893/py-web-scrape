from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit
from linkTree import build_link_tree_and_scrape
import json
import sys

class WebScraperApp(QWidget):
    def __init__(self, parent=None):
        super(WebScraperApp, self).__init__(parent)
        self.setWindowTitle("Web Scraper")

        self.layout = QVBoxLayout()

        self.url_label = QLabel("Enter Website URL:")
        self.url_input = QLineEdit()

        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)

        self.text_area = QTextEdit()

        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.text_area)

        self.setLayout(self.layout)

    def start_scraping(self):
        url = self.url_input.text()
        data = build_link_tree_and_scrape(url)
        self.text_area.setText(json.dumps(data, indent=4, ensure_ascii=False))


def main():
    app = QApplication(sys.argv)
    scraper_app = WebScraperApp()
    scraper_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
