import sys
import sqlite3
import csv
import os
import sys
import webbrowser

from typing import List, Any, Dict
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QDateEdit, QFormLayout, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton, QToolBar, QStatusBar)
from datetime import datetime

# macos
# pyinstaller --onefile --windowed -i images/MyIcon.icns --add-data real_estate_info.db:. ColoradoRealEstateSearch.py
# windows
# python -m PyInstaller --onefile -i images/icon32.ico --add-data real_estate_info.db:. ColoradoRealEstateSearch.py

class Template(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setGeometry(1000, 600, 1000, 600)
        self.setWindowTitle('Real Estate Information Search')
        self.tables = {
            'Active Associate Brokers' : QAction('Active Associate Brokers', self),
            'Active HOAs' : QAction('Active HOAs', self),
            'Active Individual Proprietors' : QAction('Active Individual Proprietors', self),
            'Active Real Estate Companies' : QAction('Active Real Estate Companies', self),
            'Active Responsible Brokers' : QAction('Active Responsible Brokers', self),
            'Active Subdivision Developers' : QAction('Active Subdivision Developers', self),
            'El Paso County Parcels' : QAction('El Paso County Parcels', self)
        }
        toolbar = QToolBar()
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)
        for table_name, toolbar_button in self.tables.items():
            self.create_toolbar_actions(table_name, toolbar_button, toolbar)
        self.setStatusBar(QStatusBar(self))
        self.swap_to_main_layout()
        self.left_column_values:List[tuple[str, QLineEdit]] = []
        self.right_column_values:List[tuple[str, QLineEdit]] = []
        self.querying_table_name = None
        self.querying_table_columns = None
        self.querying_table_google_links:Dict[int, str] = {}
        self.path_to_app = self.resolve_app_path()

    def create_toolbar_actions(self, table_name:str, toolbar_button:QAction, toolbar:QToolBar) -> None:
        toolbar_button.setStatusTip(f'Click to query {table_name}')
        toolbar_button.setCheckable(True)
        toolbar_button.triggered.connect(lambda: self.swap_to_query_layout(table_name))
        toolbar.addAction(toolbar_button)

    def uncheck_toolbar_buttons(self) -> None:
        for toolbar_button in self.tables.values():
            if toolbar_button.isChecked():
                toolbar_button.setChecked(False)

    def resolve_app_path(self) -> str:
        if getattr(sys, 'frozen', False):
            app_path = sys._MEIPASS
        elif __file__:
            app_path = os.path.dirname(os.path.abspath(__file__))
        return app_path

    def swap_to_query_layout(self, table_name:str) -> None:
        self.setWindowTitle(f'Query {table_name}')
        self.uncheck_toolbar_buttons()
        self.tables[table_name].setChecked(True)
        self.querying_table_columns = [col for col in self.get_table_column_titles(table_name)]
        self.querying_table_name = table_name.replace(' ', '')
        self.left_column_values.clear()
        self.right_column_values.clear()
        left_layout = QFormLayout()
        left_layout.setFormAlignment(Qt.AlignmentFlag.AlignAbsolute)
        right_layout = QFormLayout()
        right_layout.setFormAlignment(Qt.AlignmentFlag.AlignAbsolute)
        for count, column_name in enumerate(self.querying_table_columns):
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
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def swap_to_main_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Select a table from the ribbon to run queries against it."))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def swap_to_table_layout(self, results:List[Any]) -> None:
        table = QTableWidget()
        table.setRowCount(len(results))
        table.setColumnCount(len(self.querying_table_columns))
        if self.querying_table_name == 'ElPasoCountyParcels':
            headers = self.querying_table_columns
        else:
            headers = ['Google Link'] + self.querying_table_columns
        table.setHorizontalHeaderLabels(headers)
        for row_i, row in enumerate(results):
            if self.querying_table_name == 'ElPasoCountyParcels':
                for column_i, column in enumerate(row):
                    item = QTableWidgetItem(str(column))
                    table.setItem(row_i, column_i, item)
            else:
                google_link = self.get_google_search_link(row)
                self.add_link_to_dict(row_i, google_link)
                link_item = QTableWidgetItem('Double Click to Google')
                table.setItem(row_i, 0, link_item)
                for column_i, column in enumerate(row):
                    item = QTableWidgetItem(str(column))
                    table.setItem(row_i, column_i + 1, item)
        table.cellClicked.connect(self.google_in_browser)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        export_button = QPushButton('Export to CSV')
        export_func = lambda: self.export_to_csv(results)
        export_button.clicked.connect(export_func)
        layout.addWidget(export_button)
        layout.addWidget(table)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def export_to_csv(self, results:List[Any]) -> None:
        dt = datetime.now().strftime('%Y-%m-%d_%H-%M')
        csv_name = f'{self.querying_table_name}_{dt}.csv'
        file_path_and_name = QFileDialog.getSaveFileName(self, self.tr('Select Location for CSV File'), csv_name)
        with open(file_path_and_name[0], 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(self.querying_table_columns)
            writer.writerows(results)

    def get_table_column_titles(self, table_name:str) -> List[str]:
        conn = sqlite3.connect(os.path.join(self.path_to_app, 'real_estate_info.db'))
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name.replace(" ", "")} LIMIT 1;')
        columns = cursor.description
        names = [column[0] for column in columns]
        cursor.close()
        return names

    def get_google_search_link(self, row:List[str]) -> str:
        if self.querying_table_name == 'ElPasoCountyParcels':
            return False
        elif self.querying_table_name in ['ActiveAssociateBrokers', 'ActiveIndividualProprietors', 'ActiveResponsibleBrokers']:
            first_name_index = self.querying_table_columns.index('FirstName')
            last_name_index = self.querying_table_columns.index('LastName')
            name = (str(row[first_name_index]), str(row[last_name_index]))
        elif self.querying_table_name == 'ActiveHOAs':
            name_index = self.querying_table_columns.index('DesignatedAgent')
            name = str(row[name_index]).split(' ')
        elif self.querying_table_name in ['ActiveRealEstateCompanies', 'ActiveSubdivisionDevelopers']:
            name_index = self.querying_table_columns.index('SupervisorName')
            name = str(row[name_index]).split(' ')
        if self.querying_table_name == 'ActiveIndividualProprietors':
            zip_index = self.querying_table_columns.index('MailZipCode')
        else:
            zip_index = self.querying_table_columns.index('ZipCode')
        zip_code = str(row[zip_index])
        name = '+'.join(name)
        return f'https://www.google.com/search?q={name}+{zip_code}'
    
    def add_link_to_dict(self, row_i:int, google_link:str) -> None:
        self.querying_table_google_links[row_i] = google_link

    def google_in_browser(self, row, column) -> None:
        if column != 0 or self.querying_table_name == 'ElPasoCountyParcels':
            pass
        else:
            google_link = self.querying_table_google_links[int(row)]
            webbrowser.open_new(google_link)

    def submit_query(self) -> None:
        condition_columns = []
        condition_values = []
        for column_name, query_value in self.left_column_values:
            stripped_value = query_value.text().strip()
            if stripped_value != '':
                if stripped_value in ['1/1/00', '1/1/2000']:
                    continue
                else:
                    condition_columns.append(column_name)
                    condition_values.append(stripped_value)
        for column_name, query_value in self.right_column_values:
            stripped_value = query_value.text().strip()
            if stripped_value != '':
                if stripped_value in ['1/1/00', '1/1/2000']:
                    continue
                else:
                    condition_columns.append(column_name)
                    condition_values.append(stripped_value)
        conditions = [f"{col} = ?" for col in condition_columns[:len(condition_values)]]
        where_clause = ' AND '.join(conditions)
        query = f"SELECT * FROM {self.querying_table_name} WHERE {where_clause}"
        results = self.query_database(sql_statement=query, condition_values=condition_values)
        self.swap_to_table_layout(results)

    def print_query(self, results:List[Any]) -> None:
        print('  |  '.join(self.querying_table_columns))
        for row in results:
            row_strs = [str(i) for i in row]
            print('  |  '.join(row_strs))

    def query_database(self, sql_statement:str, condition_values:list|None=None) -> List[Any]:
        conn = sqlite3.connect(os.path.join(self.path_to_app, 'real_estate_info.db'))
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