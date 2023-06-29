import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from bs4 import BeautifulSoup, Tag
import requests
import json

class ScraperThread(QThread):
    update = pyqtSignal(str, object)
    error = pyqtSignal(str)

    def __init__(self, root_url):
        super().__init__()
        self.root_url = root_url
        self.visited = set()

    def run(self):
        try:
            self.scrape(self.root_url)
        except Exception as e:
            self.error.emit(str(e))

    def scrape(self, url):
        self.visited.add(url)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f'Failed to retrieve page: {url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        page_data = self.parse(soup)
        self.update.emit(url, page_data)
        for link in soup.find_all('a'):
            new_url = link.get('href')
            if new_url and new_url.startswith(self.root_url) and new_url not in self.visited:
                self.scrape(new_url)

    def parse(self, soup):
        data = {}
        data['title'] = soup.title.string if soup.title else ''
        data['content'] = self.recursive_content(soup.body)
        return data

    def recursive_content(self, tag):
        if isinstance(tag, Tag):
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
                return {tag.name: tag.get_text(strip=True)}
            else:
                contents = []
                for child in tag.contents:
                    content = self.recursive_content(child)
                    if content:
                        contents.append(content)
                return contents
        else:
            return None


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Website Scraper")
        
        self.layout = QVBoxLayout()
        
        self.url_label = QLabel("URL")
        self.url_entry = QTextEdit()
        
        self.start_button = QPushButton("Start scraping")
        self.start_button.clicked.connect(self.start_scraping)
        
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.start_button)
        
        self.setLayout(self.layout)
        
    def start_scraping(self):
        self.start_button.setEnabled(False)
        self.url = self.url_entry.toPlainText()
        self.thread = ScraperThread(self.url)
        self.thread.update.connect(self.update_gui)
        self.thread.error.connect(self.error_occurred)
        self.thread.finished.connect(lambda: self.start_button.setEnabled(True))
        self.thread.start()

    def update_gui(self, url, data):
        label = QLabel(f"Scraped {url}")
        self.layout.addWidget(label)
        text = QTextEdit(json.dumps(data, indent=2))
        self.layout.addWidget(text)
        button = QPushButton("Save JSON")
        button.clicked.connect(lambda: self.save_json(url, data))
        self.layout.addWidget(button)

    def error_occurred(self, error_message):
        self.layout.addWidget(QLabel(f"Error: {error_message}"))
        self.start_button.setEnabled(True)

    def save_json(self, url, data):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "JSON Files (*.json)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                json.dump(data, f, indent=2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
