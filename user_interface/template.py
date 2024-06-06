import sys
import sqlite3

from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QApplication, QCalendarWidget, QLabel, QDateEdit, QFormLayout, QHBoxLayout, QWidget, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar, QMenuBar)

class Template(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setWindowTitle('Real Estate Information Search')
        tables = [
            'Active Associate Brokers',
            'Active HOAs',
            'Active Individual Proprietors',
            'Active Real Estate Companies',
            'Active Responsible Brokers',
            'Active Subdivision Developers',
            'El Paso County Parcels'
        ]
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)
        for table_name in tables:
            self.form_toolbar_actions(table_name, toolbar)
        self.setStatusBar(QStatusBar(self))
        self.swap_to_main_layout()
        self.left_column_values:List[tuple[str, QLineEdit]] = []
        self.right_column_values:List[tuple[str, QLineEdit]] = []
        self.querying_table = None

    def form_toolbar_actions(self, table_name:str, toolbar:QToolBar):
        button_action = QAction(table_name, self)
        button_action.setStatusTip(f'Click to query {table_name}')
        button_action.table_name = table_name
        button_action.column_names = self.get_table_column_titles(table_name)
        button_action.triggered.connect(lambda: self.swap_to_query_layout(button_action.table_name, button_action.column_names))
        toolbar.addAction(button_action)

    def swap_to_query_layout(self, table_name:str, table_columns:List[str]):
        self.querying_table = table_name.replace(' ', '')
        self.left_column_values.clear()
        self.right_column_values.clear()
        left_layout = QFormLayout()
        left_layout.setFormAlignment(Qt.AlignmentFlag.AlignAbsolute)
        right_layout = QFormLayout()
        right_layout.setFormAlignment(Qt.AlignmentFlag.AlignAbsolute)
        for count, column_name in enumerate(table_columns):
            if column_name in ['id', 'ID', 'Id']:
                continue
            if 'date' in column_name or 'Date' in column_name or 'DATE' in column_name:
                field = QDateEdit()
            else:
                field = QLineEdit()
            name = QLabel(column_name)
            if count % 2 == 0:
                left_layout.addRow(name, field)
                self.left_column_values.append((column_name, field))
            else:
                right_layout.addRow(name, field)
                self.right_column_values.append((column_name, field))
        search_button = QPushButton('Submit Query')
        search_button.clicked.connect(self.submit_query)
        right_layout.addWidget(search_button)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def swap_to_main_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Select a table from the ribbon above to run queries against it."))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_table_column_titles(self, table_name:str):
        conn = sqlite3.connect('/Users/bryanjsample/Documents/code/github/hoa_prop_managers/real_estate_info.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name.replace(" ", "")} LIMIT 1;')
        columns = cursor.description
        names = [column[0] for column in columns]
        cursor.close()
        return names
    
    def submit_query(self):
        condition_columns = []
        condition_values = []
        for column_name, query_value in self.left_column_values:
            stripped_value = query_value.text().strip()
            if stripped_value != '':
                if stripped_value == '1/1/00':
                    continue
                else:
                    condition_columns.append(column_name)
                    condition_values.append(stripped_value)
        for column_name, query_value in self.right_column_values:
            stripped_value = query_value.text().strip()
            if stripped_value != '':
                if stripped_value == '1/1/00':
                    continue
                else:
                    condition_columns.append(column_name)
                    condition_values.append(stripped_value)

        conditions = [f"{col} = ?" for col in condition_columns[:len(condition_values)]]
        where_clause = ' AND '.join(conditions)
        query = f"SELECT * FROM {self.querying_table} WHERE {where_clause}"
        results = self.query_database(sql_statement=query, condition_values=condition_values)
        print(results)

    def query_database(self, sql_statement:str, condition_values:list|None=None):
        conn = sqlite3.connect('/Users/bryanjsample/Documents/code/github/hoa_prop_managers/real_estate_info.db')
        cursor = conn.cursor()
        cursor.execute(sql_statement, condition_values)
        results = cursor.fetchall()
        cursor.close()
        return results

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Template()
    widget.show()

    sys.exit(app.exec())