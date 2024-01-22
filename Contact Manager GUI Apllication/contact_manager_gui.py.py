import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, Sequence('contact_id_seq'), primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)

class ContactManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.engine = create_engine('sqlite:///contacts.db')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.contacts = []

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.lbl_name = QLabel("Name:")
        self.lbl_name.setFont(self.get_font(style='bold', size=12))
        self.txt_name = QLineEdit()

        self.lbl_phone = QLabel("Phone:")
        self.lbl_phone.setFont(self.get_font(style='bold', size=12))
        self.txt_phone = QLineEdit()

        self.lbl_email = QLabel("Email:")
        self.lbl_email.setFont(self.get_font(style='bold', size=12))
        self.txt_email = QLineEdit()

        self.lbl_address = QLabel("Address:")
        self.lbl_address.setFont(self.get_font(style='bold', size=12))
        self.txt_address = QLineEdit()

        self.btn_add = QPushButton("Add Contact")
        self.btn_remove = QPushButton("Remove Contact")
        self.btn_update = QPushButton("Update Contact")

        self.list_contacts = QListWidget()
        self.txt_search = QLineEdit()
        self.btn_search = QPushButton("Search")

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.lbl_name)
        input_layout.addWidget(self.txt_name)
        input_layout.addWidget(self.lbl_phone)
        input_layout.addWidget(self.txt_phone)
        input_layout.addWidget(self.lbl_email)
        input_layout.addWidget(self.txt_email)
        input_layout.addWidget(self.lbl_address)
        input_layout.addWidget(self.txt_address)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_remove)
        button_layout.addWidget(self.btn_update)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.btn_search)

        form_layout = QVBoxLayout()
        form_layout.addLayout(input_layout)
        form_layout.addLayout(button_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.list_contacts)

        # Apply stylesheets for a clean and professional look
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                color: #333333;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 24px;
            }
            QLineEdit, QPushButton {
                font-size: 24px;
                padding: 8px;
                margin: 5px;
            }
            QPushButton {
                background-color: #4285f4;
                color: #ffffff;
                border: 1px solid #4285f4;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2c5aa0;
                border: 1px solid #2c5aa0;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #d3d3d3;
            }
        """)

        # Connect signals
        self.btn_add.clicked.connect(self.add_contact)
        self.btn_remove.clicked.connect(self.remove_contact)
        self.btn_update.clicked.connect(self.update_contact)
        self.btn_search.clicked.connect(self.search_contact)
        self.list_contacts.itemClicked.connect(self.display_contact_details)  # Connect the itemClicked signal

        # Load existing contacts from the database
        self.load_contacts()

        # Set up the main window
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Contact Manager')
        self.show()

    def display_contact_details(self, item):
        index = self.list_contacts.row(item)
        contact = self.contacts[index]

        details_text = f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}\nAddress: {contact.address}"

        QMessageBox.information(self, 'Contact Details', details_text)

    def add_contact(self):
        name = self.txt_name.text()
        phone = self.txt_phone.text()
        email = self.txt_email.text()
        address = self.txt_address.text()

        if name and phone:
            contact = Contact(name=name, phone=phone, email=email, address=address)
            self.session.add(contact)
            self.session.commit()

            self.contacts.append(contact)
            self.list_contacts.addItem(f"{contact.name} - {contact.phone}")
            self.clear_input_fields()
        else:
            QMessageBox.warning(self, 'Input Error', 'Name and Phone cannot be empty!')

    def remove_contact(self):
        selected_item = self.list_contacts.currentItem()

        if selected_item:
            index = self.list_contacts.row(selected_item)
            contact = self.contacts[index]

            self.session.delete(contact)
            self.session.commit()

            del self.contacts[index]
            self.list_contacts.takeItem(index)
        else:
            QMessageBox.warning(self, 'Selection Error', 'Please select a contact to remove.')

    def update_contact(self):
        selected_item = self.list_contacts.currentItem()

        if selected_item:
            index = self.list_contacts.row(selected_item)
            old_contact = self.contacts[index]

            new_name = self.txt_name.text()
            new_phone = self.txt_phone.text()
            new_email = self.txt_email.text()
            new_address = self.txt_address.text()

            if new_name and new_phone:
                old_contact.name = new_name
                old_contact.phone = new_phone
                old_contact.email = new_email
                old_contact.address = new_address

                self.session.commit()

                self.contacts[index] = old_contact
                selected_item.setText(f"{old_contact.name} - {old_contact.phone}")
                self.clear_input_fields()
            else:
                QMessageBox.warning(self, 'Input Error', 'Name and Phone cannot be empty.')
        else:
            QMessageBox.warning(self, 'Selection Error', 'Please select a contact to update.')

    def search_contact(self):
        search_text = self.txt_search.text().lower()
        self.list_contacts.clear()

        for contact in self.contacts:
            if search_text in contact.name.lower() or search_text in contact.phone.lower():
                self.list_contacts.addItem(f"{contact.name} - {contact.phone}")

    def load_contacts(self):
        contacts = self.session.query(Contact).all()
        for contact in contacts:
            self.contacts.append(contact)
            self.list_contacts.addItem(f"{contact.name} - {contact.phone}")

    def clear_input_fields(self):
        self.txt_name.clear()
        self.txt_phone.clear()
        self.txt_email.clear()
        self.txt_address.clear()

    def get_font(self, family='Segoe UI', size=12, style='', weight=QFont.Normal):
        font = self.font()
        font.setFamily(family)
        font.setPointSize(size)
        font.setStyleName(style)
        font.setWeight(weight)
        return font

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ContactManagerApp()
    sys.exit(app.exec_())
