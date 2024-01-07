import tkinter as tk
from tkinter import ttk

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero"

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        if operation == "Addition":
            result = add(num1, num2)
        elif operation == "Subtraction":
            result = subtract(num1, num2)
        elif operation == "Multiplication":
            result = multiply(num1, num2)
        else:
            result = divide(num1, num2)

        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Error: Invalid input")

def clear_inputs():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    result_label.config(text="Result: ")

# Create the main window
window = tk.Tk()
window.title("User-Friendly Calculator")

# Style configuration
style = ttk.Style()
style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='4')
style.configure('TLabel', font=('calibri', 12, 'bold'), foreground='blue')

# Entry fields for numbers
entry_num1 = ttk.Entry(window, font=('calibri', 12, 'bold'), justify='center')
entry_num1.grid(row=0, column=0, padx=5, pady=5)

entry_num2 = ttk.Entry(window, font=('calibri', 12, 'bold'), justify='center')
entry_num2.grid(row=0, column=1, padx=5, pady=5)

# Operation dropdown
operations = ["Addition", "Subtraction", "Multiplication", "Division"]
operation_var = tk.StringVar()
operation_var.set(operations[0])  # Default operation
operation_menu = ttk.Combobox(window, textvariable=operation_var, values=operations, font=('calibri', 12, 'bold'))
operation_menu.grid(row=0, column=2, padx=5, pady=5)

# Buttons
calculate_button = ttk.Button(window, text="Calculate", command=calculate)
calculate_button.grid(row=1, column=0, pady=10, padx=5, sticky='ew')

clear_button = ttk.Button(window, text="Clear", command=clear_inputs)
clear_button.grid(row=1, column=1, pady=10, padx=5, sticky='ew')

# Display result
result_label = ttk.Label(window, text="Result: ", font=('calibri', 12, 'bold'))
result_label.grid(row=2, column=0, columnspan=3, pady=10)

# Set fixed window size
window.resizable(False, False)

# Run the GUI
window.mainloop()
