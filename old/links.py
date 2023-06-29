import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import requests

class ScraperThread(QThread):
    notifyProgress = pyqtSignal(str)

    def __init__(self, base_url, div, cls, link_contains):
        QThread.__init__(self)
        self.base_url = base_url
        self.div = div
        self.cls = cls
        self.link_contains = link_contains

    def run(self):
        self.notifyProgress.emit("Scraping links started")
        try:
            response = requests.get(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all(self.div, class_=self.cls):
                if self.link_contains in link.get('href'):
                    self.notifyProgress.emit("Found link: " + link.get('href'))
        except Exception as e:
            self.notifyProgress.emit("Error: " + str(e))


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.urlInput = QLineEdit()
        self.urlInput.setText("https://python.langchain.com/docs/get_started")
        layout.addWidget(QLabel("Base Url:"))
        layout.addWidget(self.urlInput)

        self.divInput = QLineEdit()
        self.divInput.setText("a")
        layout.addWidget(QLabel("Div for Links:"))
        layout.addWidget(self.divInput)

        self.classInput = QLineEdit()
        self.classInput.setText("menu__link")
        layout.addWidget(QLabel("Class for Links:"))
        layout.addWidget(self.classInput)

        self.containsInput = QLineEdit()
        self.containsInput.setText("docs")
        layout.addWidget(QLabel("Links to Scrape Contains:"))
        layout.addWidget(self.containsInput)

        self.goButton = QPushButton("Go")
        self.goButton.clicked.connect(self.startScraping)
        layout.addWidget(self.goButton)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopScraping)
        layout.addWidget(self.stopButton)

        self.output = QTextEdit()
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def startScraping(self):
        self.scraper = ScraperThread(self.urlInput.text(), self.divInput.text(), self.classInput.text(), self.containsInput.text())
        self.scraper.notifyProgress.connect(self.updateOutput)
        self.scraper.start()

    def stopScraping(self):
        self.scraper.terminate()

    def updateOutput(self, text):
        self.output.append(text)

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
