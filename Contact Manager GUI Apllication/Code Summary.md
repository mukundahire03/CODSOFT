### Contact Manager App

This is a simple Contact Manager application implemented in Python using the PyQt5 library for the graphical user interface (GUI) and SQLAlchemy for database interactions. The application allows users to manage their contacts by adding, removing, updating, and searching for contacts.

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Databases](#database)
- [License](#license)

![Contact Manager App](https://github.com/mukundahire03/CODSOFT/blob/main/Contact%20Manager%20GUI%20Apllication/Screenshot%20from%202024-01-22%2017-32-31.png)

### Installation

1. Ensure you have Python installed on your system.

2. Install required dependencies by running:

       pip install PyQt5 SQLAlchemy

3. Run the application using the following command:

        python contact_manager.py

### Usage

To run the Contact Manager application, execute the script `contact_manager.py`. The main window will appear, providing a user-friendly interface for managing contacts.

### Features

- **Add Contact:** Users can add new contacts by providing their name, phone number, email, and address.

- **Remove Contact:** Contacts can be removed by selecting them from the contact list and clicking the "Remove Contact" button.

- **Update Contact:** Users can update the details of existing contacts by selecting them from the contact list, modifying the information, and clicking the "Update Contact" button.

- **Search Contact:** The application supports searching for contacts based on their name or phone number. Users can enter search criteria in the search bar and click the "Search" button to filter the contact list.

- **Display Contact Details:** Clicking on a contact in the list displays detailed information about the selected contact, including name, phone number, email, and address.

- **Styling:** The GUI is styled using CSS-like style sheets to enhance the visual appeal of the application.

### Dependencies

- **PyQt5:** A set of Python bindings for Qt application framework, used for building the GUI.

- **SQLAlchemy:** A SQL toolkit and Object-Relational Mapping (ORM) library for Python, employed for database interactions.

### Database

The application uses a SQLite database ('contacts.db') to store contact information persistently. The database schema includes a 'contacts' table with columns for contact ID, name, phone number, email, and address.

### License

This Contact Manager Application is licensed under the [MIT License](LICENSE).
