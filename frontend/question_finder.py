# question_finder.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QTextBrowser, QListWidgetItem,
    QCheckBox
)

from PyQt5.QtCore import Qt

from resource_handler import ResourceHandler

class QuestionItemWidget(QWidget):
    def __init__(self, topic, question_text, marks):
        super().__init__()
        
        # Main layout for the custom widget
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins for compact display

        # Topic label
        topic_label = QLabel(f"Topic: {topic}")
        topic_label.setStyleSheet("font-weight: bold; color: #333333;")
        
        # Question text label
        question_label = QLabel(f"Question: {question_text}")
        question_label.setWordWrap(True)
        question_label.setStyleSheet("color: #555555;")
        
        # Marks label
        marks_label = QLabel(f"Marks: {marks}")
        marks_label.setStyleSheet("color: #777777;")
        
        # Add labels to the layout
        layout.addWidget(topic_label)
        layout.addWidget(question_label)
        layout.addWidget(marks_label)
        
        self.setLayout(layout)

class QuestionFinderPage(QWidget):
    def __init__(self, resource_handler: ResourceHandler):
        super().__init__()
        self.resource_handler = resource_handler

        self.search_params = {
            "topics": [],
            "papers": [],
            "years": []
        }
        self.questions = []

        # Main horizontal layout for the three sections
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Create each section and add them to the main layout
        self.create_query_section(main_layout)
        self.create_question_list_section(main_layout)
        self.create_question_display_section(main_layout)
        
    def create_query_section(self, layout: QHBoxLayout):
        # Query & Selection Parameters Section
        query_widget = QWidget()
        query_layout = QVBoxLayout()
        query_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        query_widget.setLayout(query_layout)

        # Set minimum/maximum width for the query section
        query_widget.setMaximumWidth(500)
        query_widget.setMinimumWidth(400)
        
        # Add search fields and button
        search_label = QLabel("Search Query:")
        search_input = QLineEdit()
        self.search_params["search"] = search_label.text

        query_layout.addWidget(search_label)
        query_layout.addWidget(search_input)
        
        # Filter topic checkboxes
        topics = ["Databases", "OS", "CPU"]

        filter_topics_label = QLabel("Topics:")
        query_layout.addWidget(filter_topics_label)
        
        for topic in topics:
            checkbox = QCheckBox(topic)
            checkbox.setChecked(True)
            self.search_params["topics"].append([topic, checkbox.isChecked])
            query_layout.addWidget(checkbox)

        # Filter paper checkboxes
        
        papers = ["Paper 1", "Paper 2"]
        
        filter_papers_label = QLabel("\nPapers:")
        query_layout.addWidget(filter_papers_label)
        
        for paper in papers:
            checkbox = QCheckBox(paper)
            checkbox.setChecked(True)
            self.search_params["papers"].append([paper, checkbox.isChecked])
            query_layout.addWidget(checkbox)

        # Filter year checkboxes
        
        years = ["2023", "2022", "2021", "2020", "2019"]
        
        filter_years_label = QLabel("\nYears:")
        query_layout.addWidget(filter_years_label)
        
        for year in years:
            checkbox = QCheckBox(year)
            checkbox.setChecked(True)
            self.search_params["years"].append([year, checkbox.isChecked])
            query_layout.addWidget(checkbox)

        # Search button

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_questions)
        query_layout.addWidget(search_button)
        
        # Add the query section to the main horizontal layout
        layout.addWidget(query_widget, 1)

    def create_question_list_section(self, layout):
        question_list_widget = QWidget()
        question_list_layout = QVBoxLayout()
        question_list_layout.setAlignment(Qt.AlignTop)
        question_list_widget.setLayout(question_list_layout)
        
        # Set minimum/maximum width for the question list section
        question_list_widget.setMinimumWidth(500)
        question_list_widget.setMaximumWidth(900)
        
        # Create the QListWidget to display questions
        self.question_list = QListWidget()
        
        # Populate the question list with custom widgets
        for question in self.questions:
            topic = question["topics"]
            question_text = question["question"]
            marks = question["marks"]
            
            # Create a custom QuestionItemWidget for each question
            item_widget = QuestionItemWidget(topic, question_text, marks)
            
            # Create a QListWidgetItem to hold the custom widget
            list_item = QListWidgetItem(self.question_list)
            list_item.setSizeHint(item_widget.sizeHint())  # Adjust item size
            
            # Add the custom widget to the QListWidget
            self.question_list.addItem(list_item)
            self.question_list.setItemWidget(list_item, item_widget)
        
        # Add list widget to the layout
        question_list_layout.addWidget(self.question_list)
        
        layout.addWidget(question_list_widget, 2)

    def create_question_display_section(self, layout: QHBoxLayout):
        # Selected Question Display Section
        question_display_widget = QWidget()
        question_display_layout = QVBoxLayout()
        question_display_widget.setLayout(question_display_layout)
        
        # Text browser to display selected question details
        question_display = QTextBrowser()
        question_display.setText("Select a question to view details here.")
        
        # Add text browser to the layout
        question_display_layout.addWidget(question_display)
        
        # Add the question display section to the main horizontal layout
        layout.addWidget(question_display_widget, 2)

    def search_questions(self):
        topics = set([topic for topic, isChecked in self.search_params["topics"] if isChecked()])
        papers = [paper for paper, isChecked in self.search_params["papers"] if isChecked()]
        years =  [year  for  year, isChecked in self.search_params["years"]  if isChecked()]


        self.questions = []
        for question in self.resource_handler.questions:
            if question.paper in papers and question.year in years and bool(question.topics & topics):
                self.questions.append(question)