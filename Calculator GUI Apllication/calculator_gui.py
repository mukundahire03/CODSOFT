import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.expression = ""
        self.history = ""

        main_layout = QVBoxLayout()

        history_display = QTextEdit(self)
        history_display.setReadOnly(True)
        main_layout.addWidget(history_display)

        input_display = QLineEdit(self)
        input_display.setReadOnly(True)
        input_display.setAlignment(Qt.AlignRight)  # Set right alignment
        main_layout.addWidget(input_display)

        button_layout = QGridLayout()

        buttons = [
            ('(', 0, 0, 1, 1), (')', 0, 1, 1, 1), ('C', 0, 2, 1, 1), ('/', 0, 3, 1, 1),
            ('7', 1, 0, 1, 1), ('8', 1, 1, 1, 1), ('9', 1, 2, 1, 1), ('*', 1, 3, 1, 1),
            ('4', 2, 0, 1, 1), ('5', 2, 1, 1, 1), ('6', 2, 2, 1, 1), ('-', 2, 3, 1, 1),
            ('1', 3, 0, 1, 1), ('2', 3, 1, 1, 1), ('3', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('0', 4, 0, 1, 1), ('.', 4, 1, 1, 1), ('⌫', 4, 2, 1, 1), ('=', 4, 3, 1, 1),
            ('Clear History', 5, 0, 1, 4),  # Added 'Clear History' button
        ]

        for text, row, col, rowspan, colspan in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            if text == 'Clear History':
                button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            button_layout.addWidget(button, row, col, rowspan, colspan)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.setWindowTitle('Calculator')

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.on_button_click('=')
        elif key == Qt.Key_Backspace:
            self.on_button_click('⌫')
        elif key == Qt.Key_Delete:
            self.on_button_click('⌦')
        elif key == Qt.Key_Escape:
            self.close()
        elif event.text().isdigit() or event.text() in ['+', '-', '*', '/', '.', '(', ')', '%']:
            self.on_button_click(event.text())

    def on_button_click(self, button_text):
        CLEAR_HISTORY = 'Clear History'

        if button_text == '=':
            try:
                result = str(eval(self.expression))
                self.history += f"{self.expression} = {result}\n"
                self.expression = result
            except Exception as e:
                self.history += f"Error: {e}\n"
                self.expression = "Error"
        elif button_text == 'C':
            self.expression = ""
        elif button_text == '⌫':  # Backspace
            self.expression = self.expression[:-1]
        elif button_text == CLEAR_HISTORY:
            self.clear_history()
        else:
            self.expression += button_text

        self.update_displays()

    def clear_history(self):
        self.history = ""

    def update_displays(self):
        input_display = self.findChild(QLineEdit)
        history_display = self.findChild(QTextEdit)

        if input_display and history_display:
            input_display.setText(self.expression)
            history_display.setPlainText(self.history)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())
