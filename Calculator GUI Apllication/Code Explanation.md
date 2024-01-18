## 1. Importing Modules:

        import sys
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout,
         QPushButton,QLineEdit, QTextEdit
        from PyQt5.QtCore import Qt

Here, necessary modules are imported. sys is for system-related operations, and PyQt5.QtWidgets and PyQt5.QtCore are from the PyQt5 library for building the GUI.

## 2. Class Definition:

        class CalculatorApp(QWidget):
            def __init__(self):
                super().__init__()
        
                self.init_ui()

The CalculatorApp class is defined, inheriting from QWidget. The constructor initializes the UI using the init_ui method.

## 3. Initializing UI:

        def init_ui(self):
            # ... (omitted for brevity)

The init_ui method sets up the initial user interface for the calculator. It creates various widgets such as QLineEdit for displaying input, QTextEdit for displaying history, and QGridLayout for arranging buttons.

## 4. Button Layout:

        buttons = [
            # ... (button configurations)
        ]

The buttons list contains configurations for different buttons on the calculator, specifying the text, position, and size of each button.

## 5. Button Connections:

        for text, row, col, rowspan, colspan in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            button_layout.addWidget(button, row, col, rowspan, colspan)

This loop creates QPushButton objects, connects their click signals to the on_button_click method, and adds them to the QGridLayout.

## 6. Key Press Events:

        def keyPressEvent(self, event):
            # ... (handling key events)

The keyPressEvent method handles keyboard events, allowing the user to interact with the calculator using both mouse clicks and keyboard input.

## 7. Button Click Handling:

        def on_button_click(self, button_text):
            # ... (handling button clicks)

The on_button_click method is called when a button is clicked (either by the mouse or through keyboard input). It updates the calculator's state based on the button clicked.

## 8. Clearing History:

        def clear_history(self):
            self.history = ""

The clear_history method resets the history.

## 9. Updating Displays:

        def update_displays(self):
            # ... (updating input and history displays)

The update_displays method updates the input and history displays with the current calculator state.

## 10. Main Execution:

          if __name__ == '__main__':
              app = QApplication(sys.argv)
              calculator = CalculatorApp()
              calculator.show()
              sys.exit(app.exec_())

The main block initializes the QApplication, creates an instance of the CalculatorApp, shows it, and starts the application event loop.

## NOTE:

Overall, the code defines a simple calculator GUI using PyQt5, with buttons for numeric input, operators, and special functions. It handles both mouse clicks and keyboard input for user interaction. The calculator supports basic arithmetic operations, history tracking, and error handling.
