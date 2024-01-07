import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QListWidget, QComboBox, QCheckBox, QInputDialog, QFileDialog, QCalendarWidget, QDateEdit, QLabel, \
    QMainWindow, QAction, QMenu, QToolBar, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QDate
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = create_engine('sqlite:///todo.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.tasks = []

        self.init_ui()

    def init_ui(self):
        # ... (unchanged code)

    def create_actions(self):
        self.save_action = QAction(QIcon('icons/save.png'), 'Save', self)
        self.save_action.triggered.connect(self.save_tasks)

        self.open_action = QAction(QIcon('icons/open.png'), 'Open', self)
        self.open_action.triggered.connect(self.load_tasks)

        self.exit_action = QAction(QIcon('icons/exit.png'), 'Exit', self)
        self.exit_action.triggered.connect(self.close)

    def add_task(self):
        task_text = self.task_entry.text().strip()
        if task_text:
            new_task = Task(
                title=task_text,
                description=self.description_entry.text().strip(),
                priority=self.priority_combo.currentText(),
                due_date=self.due_date_entry.date().toPyDate()
            )
            with self.Session() as session:
                session.add(new_task)
                session.commit()
                self.load_tasks()
            self.clear_input_fields()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a task.')

    def save_tasks(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Tasks', '', 'Todo Files (*.todo);;All Files (*)')
        if file_name:
            with self.Session() as session:
                tasks = session.query(Task).all()
                with open(file_name, 'w') as file:
                    for task in tasks:
                        file.write(f"{task.title}\n")
                        file.write(f"Description: {task.description}\n")
                        file.write(f"Priority: {task.priority}\n")
                        file.write(f"Due Date: {task.due_date}\n")
                        file.write(f"Completed: {task.completed}\n")
                        file.write('\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    sys.exit(app.exec_())
