# main.py
from PyQt5.QtWidgets import QApplication, QMainWindow
from question_finder import QuestionFinderPage
import sys

from resource_handler import ResourceHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resource_handler = ResourceHandler()
        
        # Set the main window properties
        self.setWindowTitle("Question Query Interface")
        self.setGeometry(100, 100, 1700, 1300)
        
        # Create an instance of QuestionFinderPage and set it as the central widget
        self.question_finder_page = QuestionFinderPage(self.resource_handler)
        self.setCentralWidget(self.question_finder_page)

# Main Application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
