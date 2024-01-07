import tkinter as tk
from tkinter import messagebox
import secrets
import string

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator App")

        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

        self.length_entry = tk.Entry(master)
        self.length_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.include_symbols_var = tk.BooleanVar(value=True)
        self.include_symbols_checkbox = tk.Checkbutton(master, text="Include Symbols", variable=self.include_symbols_var)
        self.include_symbols_checkbox.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_and_display_password)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.strength_label = tk.Label(master, text="")
        self.strength_label.grid(row=5, column=0, columnspan=2)

    def generate_and_display_password(self):
        try:
            length = int(self.length_entry.get())
            if length > 0:
                characters = string.ascii_letters + string.digits
                if self.include_symbols_var.get():
                    characters += string.punctuation

                password = ''.join(secrets.choice(characters) for _ in range(length))
                self.result_label.config(text=f"Generated Password: {password}")

                # Assess password strength
                strength = self.assess_password_strength(password)
                self.strength_label.config(text=f"Password Strength: {strength}")

            else:
                messagebox.showerror("Error", "Please enter a valid positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid positive integer.")

    def copy_to_clipboard(self):
        password = self.result_label.cget("text").split(": ")[1]
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        self.master.update()
        messagebox.showinfo("Success", "Password copied to clipboard!")

    def assess_password_strength(self, password):
        # A simple assessment based on the presence of various character types
        character_types = [any(c.islower() for c in password),
                           any(c.isupper() for c in password),
                           any(c.isdigit() for c in password),
                           any(c in string.punctuation for c in password)]

        strength = sum(character_types)
        return strength

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
