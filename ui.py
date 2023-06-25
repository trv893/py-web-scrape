from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal

from bs4 import BeautifulSoup
import requests
import sys

class ScraperThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, url, tag, cls, prepend, filename):
        QThread.__init__(self)
        self.url = url
        self.tag = tag
        self.cls = cls
        self.prepend = prepend
        self.filename = filename

    def run(self):
        while self.url is not None:
            self.signal.emit(f"Scraping URL: {self.url}")
            soup = self.get_soup_from_url(self.url)
            if soup is not None:
                self.write_text_to_file(soup, self.filename)
                self.url = self.get_next_url(soup, self.prepend)
            else:
                break
        self.signal.emit("Scraping completed.")

    def get_soup_from_url(self, url):
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.signal.emit(f"Something went wrong: {err}")
            return None
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def write_text_to_file(self, soup, filename):
        with open(filename, 'a') as f:
            f.write(soup.get_text())

    def get_next_url(self, soup, prepend):
        a_tag = soup.find(self.tag, class_=self.cls)
        if a_tag is not None:
            return prepend + a_tag['href']
        else:
            return None

class ScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.url_input = QLineEdit(self)
        self.tag_input = QLineEdit(self)
        self.class_input = QLineEdit(self)
        self.prepend_input = QLineEdit(self)
        self.filename_input = QLineEdit(self)
        self.log_label = QLabel(self)

        self.start_button = QPushButton('Start scraping', self)
        self.start_button.clicked.connect(self.start_scraping)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Base URL:"))
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(QLabel("Tag to search for:"))
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(QLabel("Class to search for:"))
        self.layout.addWidget(self.class_input)
        self.layout.addWidget(QLabel("URL to prepend:"))
        self.layout.addWidget(self.prepend_input)
        self.layout.addWidget(QLabel("Output filename:"))
        self.layout.addWidget(self.filename_input)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.log_label)

        self.thread = None

    def start_scraping(self):
        url = self.url_input.text()
        tag = self.tag_input.text()
        cls = self.class_input.text()
        prepend = self.prepend_input.text()
        filename = self.filename_input.text()

        self.thread = ScraperThread(url, tag, cls, prepend, filename)
        self.thread.signal.connect(self.update_log)
        self.thread.start()

    def update_log(self, text):
        self.log_label.setText(text)

def main():
    app = QApplication(sys.argv)
    ex = ScraperApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
