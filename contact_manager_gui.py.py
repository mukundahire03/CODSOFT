import tkinter as tk
from tkinter import ttk
import pandas as pd

class ContactManager:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone_number, email, address):
        self.contacts[name] = {'phone_number': phone_number, 'email': email, 'address': address}

    def view_contact_list(self):
        for name, info in self.contacts.items():
            print(f"{name}: {info['phone_number']}")

    def save_to_excel(self, filename='contact_list.xlsx'):
        df = pd.DataFrame(self.contacts).T
        df.to_excel(filename, index_label='Name')

class ContactManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")

        self.contact_manager = ContactManager()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Phone Number:").grid(row=1, column=0, sticky="e")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Email:").grid(row=2, column=0, sticky="e")
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Address:").grid(row=3, column=0, sticky="e")
        self.address_entry = ttk.Entry(self.root)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self.root, text="Add Contact", command=self.add_contact).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="View Contact List", command=self.view_contact_list).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Save to Excel", command=self.save_to_excel).grid(row=6, column=0, columnspan=2, pady=10)

    def add_contact(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        self.contact_manager.add_contact(name, phone_number, email, address)
        self.clear_entries()

    def view_contact_list(self):
        self.contact_manager.view_contact_list()

    def save_to_excel(self):
        self.contact_manager.save_to_excel()
        print("Contact list saved to Excel file.")

    def clear_entries(self):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_entry.delete(0, "end")

def main():
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
