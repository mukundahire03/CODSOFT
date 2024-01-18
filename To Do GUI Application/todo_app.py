import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMainWindow, QAction, QMessageBox, QFileDialog, QDialog, QDateEdit, QFormLayout, QLabel, QListWidget, QCheckBox, QListWidgetItem, QInputDialog, QComboBox, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


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

        self.priorities = ['High', 'Medium', 'Low']
        self.init_ui()
    def toggle_task_completion(self, state):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task = selected_item.data(Qt.UserRole)
            task.completed = not task.completed
            with self.Session() as session:
                session.commit()
            self.update_task_list()
            QMessageBox.information(self, 'Task Updated', f'Task "{task.title}" completion status updated.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a task to update.')

    def init_ui(self):
        self.setWindowTitle('Todo List App')
        self.setGeometry(100, 100, 600, 400)

        self.create_actions()
        self.create_menus()
        self.create_toolbar()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.on_accepted)
        buttons.rejected.connect(self.on_rejected)

        layout = QVBoxLayout()
        layout.addWidget(buttons)
        self.setLayout(layout)

        self.setup_ui_components()
        self.setup_layout()
        self.setup_connections()
        self.setStyleSheet("QMainWindow {background: #f0f0f0;} QPushButton {background: #4CAF50; color: white;}")
        self.due_date_entry.setDate(QDate.currentDate())
        
    def on_accepted(self):
        self.accept()
        
    def on_rejected(self):
        self.close()  
        
    def create_actions(self):
        self.save_action = QAction(QIcon('/media/mukundahire03/Mukund_Ahire/Work/Internship/Codsoft/To Do Application/icons/save.png'), 'Save', self)
        self.save_action.triggered.connect(self.save_tasks)

        self.open_action = QAction(QIcon('/media/mukundahire03/Mukund_Ahire/Work/Internship/Codsoft/To Do Application/icons/open.png'), 'Open', self)
        self.open_action.triggered.connect(self.load_tasks)

        self.exit_action = QAction(QIcon('/media/mukundahire03/Mukund_Ahire/Work/Internship/Codsoft/To Do Application/icons/exit.png'), 'Exit', self)
        self.exit_action.triggered.connect(self.close)

    def create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

    def create_toolbar(self):
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.open_action)
        toolbar.addSeparator()
        toolbar.addAction(self.exit_action)

    def setup_ui_components(self):
        self.task_entry = QLineEdit()
        self.description_entry = QLineEdit()
        self.priority_combo = QComboBox()
        self.due_date_entry = QDateEdit()
        self.due_date_entry.setDisplayFormat("dd/MM/yyyy")
        self.task_list = QListWidget()
        self.complete_checkbox = QCheckBox('Complete Task')
        
        self.priority_combo.addItems(self.priorities)

    def setup_layout(self):
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel('Task Title:'))
        input_layout.addWidget(self.task_entry)
        input_layout.addWidget(QLabel('Description:'))
        input_layout.addWidget(self.description_entry)
        input_layout.addWidget(QLabel('Priority:'))
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(QLabel('Due Date:'))
        input_layout.addWidget(self.due_date_entry)
        input_layout.addWidget(self.complete_checkbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton('Add Task', clicked=self.add_task))
        button_layout.addWidget(QPushButton('Remove Task', clicked=self.remove_task))
        button_layout.addWidget(QPushButton('Edit Task', clicked=self.edit_task))

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addLayout(button_layout)

    def setup_connections(self):
        self.complete_checkbox.stateChanged.connect(self.toggle_task_completion)
        self.task_list.itemSelectionChanged.connect(self.load_task_details)

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

    def load_tasks(self):
        with self.Session() as session:
            self.tasks = session.query(Task).all()
            self.update_task_list()

    def load_task_details(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task = selected_item.data(Qt.UserRole)
            self.description_entry.setText(task.description)
            self.priority_combo.setCurrentText(task.priority)
            if task.due_date:
                self.due_date_entry.setDate(QDate.fromString(str(task.due_date), Qt.ISODate))
            else:
                self.due_date_entry.setDate(QDate.currentDate())
            self.complete_checkbox.setChecked(task.completed)
        else:
            self.clear_input_fields()

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            item = QListWidgetItem(task.title)
            item.setData(Qt.UserRole, task)
            if task.completed:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
            self.task_list.addItem(item)

    def clear_input_fields(self):
        self.task_entry.clear()
        self.description_entry.clear()
        self.priority_combo.setCurrentIndex(0)
        self.due_date_entry.setDate(QDate.currentDate())
        self.complete_checkbox.setChecked(False)

    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            removed_task = selected_item.data(Qt.UserRole)
            with self.Session() as session:
                session.delete(removed_task)
                session.commit()
                self.load_tasks()
            QMessageBox.information(self, 'Task Removed', f'Task "{removed_task.title}" has been removed.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a task to remove.')

    def edit_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_to_edit = selected_item.data(Qt.UserRole)
            dialog = TodoApp.TaskEditDialog(task_to_edit, parent=self)
            if dialog.exec_():
                with self.Session() as session:
                    session.commit()
                self.load_tasks()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a task to edit.')

    class TaskEditDialog(QDialog):
        def __init__(self, task, parent=None):
            super(TodoApp.TaskEditDialog, self).__init__(parent)
            self.task = task
            self.setup_ui()

        def setup_ui(self):
            self.setWindowTitle('Edit Task')
            layout = QVBoxLayout()

            title_label = QLabel('Task Title:')
            title_entry = QLineEdit(self.task.title)
            description_label = QLabel('Description:')
            description_entry = QLineEdit(self.task.description)
            priority_label = QLabel('Priority:')
            priority_combo = QComboBox()
            priority_combo.addItems(['High', 'Medium', 'Low'])
            priority_combo.setCurrentText(self.task.priority)
            due_date_label = QLabel('Due Date:')
            due_date_entry = QDateEdit()
            due_date_entry.setDisplayFormat("dd/MM/yyyy")
            due_date_entry.setDate(QDate.fromString(str(self.task.due_date), Qt.ISODate) if self.task.due_date else QDate.currentDate())
            complete_checkbox = QCheckBox('Complete Task')
            complete_checkbox.setChecked(self.task.completed)

            form_layout = QFormLayout()
            form_layout.addRow(title_label, title_entry)
            form_layout.addRow(description_label, description_entry)
            form_layout.addRow(priority_label, priority_combo)
            form_layout.addRow(due_date_label, due_date_entry)
            form_layout.addRow(complete_checkbox)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            form_layout.addRow(buttons)

            layout.addLayout(form_layout)
            self.setLayout(layout)

            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)

        def accept(self):
            self.task.title = self.findChild(QLineEdit, 'title_entry').text()
            self.task.description = self.findChild(QLineEdit, 'description_entry').text()
            self.task.priority = self.findChild(QComboBox, 'priority_combo').currentText()
            self.task.due_date = self.findChild(QDateEdit, 'due_date_entry').date().toPyDate()
            self.task.completed = self.findChild(QCheckBox, 'complete_checkbox').isChecked()
            super().accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
