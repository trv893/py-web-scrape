from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog
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
        self.log = QTextEdit()

        self.save_button = QPushButton("Save as JSON")
        self.save_button.clicked.connect(self.save_as_json)
        self.save_button.setEnabled(False)  # Disable until scraping is done

        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.text_area)
        self.layout.addWidget(self.log)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.data = {}  # Initialize empty data

    def start_scraping(self):
        url = self.url_input.text()
        logger = []
        self.data = build_link_tree_and_scrape(url, logger)
        self.text_area.setText(json.dumps(self.data, indent=4, ensure_ascii=False))
        self.log.setText('\n'.join(logger))
        self.save_button.setEnabled(True)  # Enable the save button

    def save_as_json(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","JSON Files (*.json);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

def main():
    app = QApplication(sys.argv)
    scraper_app = WebScraperApp()
    scraper_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
