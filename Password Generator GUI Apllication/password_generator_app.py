import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QCheckBox, QSlider
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import string
import random

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Password Generator')
        self.setGeometry(300, 300, 500, 300)
        self.setWindowIcon(QIcon('icon.png'))

        font = QFont("Helvetica", 12)
        self.setFont(font)

        self.header_label = QLabel('Password Generator', self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("QLabel { color: #007AFF; font-weight: bold; }")

        self.password_label = QLabel('Generated Password:', self)
        self.password_output = QLineEdit(self)
        self.password_output.setReadOnly(True)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.clicked.connect(self.generate_password)
        self.style_smooth_button(self.generate_button, "#007AFF")

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_password)
        self.style_smooth_button(self.reset_button, "red")

        self.customization_label = QLabel('Customization Options:', self)
        self.customization_label.setStyleSheet("QLabel { color: #007AFF; font-weight: bold; }")

        self.length_label = QLabel('Password Length:', self)
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(1)
        self.length_slider.setMaximum(30)
        self.length_slider.setValue(12)

        self.uppercase_checkbox = QCheckBox('Uppercase', self)
        self.lowercase_checkbox = QCheckBox('Lowercase', self)
        self.digits_checkbox = QCheckBox('Digits', self)
        self.symbols_checkbox = QCheckBox('Symbols', self)

        self.style_smooth_checkbox(self.uppercase_checkbox)
        self.style_smooth_checkbox(self.lowercase_checkbox)
        self.style_smooth_checkbox(self.digits_checkbox)
        self.style_smooth_checkbox(self.symbols_checkbox)

        self.strength_label = QLabel('Password Strength:', self)
        self.strength_indicator = QLabel(self)
        self.strength_indicator.setAlignment(Qt.AlignCenter)
        self.strength_indicator.setStyleSheet("QLabel {font-weight: bold; }")

        layout = QGridLayout(self)
        layout.addWidget(self.header_label, 0, 0, 1, 3)
        layout.addWidget(self.password_label, 1, 0, 1, 3)
        layout.addWidget(self.password_output, 2, 0, 1, 3)
        layout.addWidget(self.customization_label, 3, 0, 1, 3)

        layout.addWidget(self.length_label, 4, 0, 1, 1)
        layout.addWidget(self.length_slider, 4, 1, 1, 2)

        layout.addWidget(self.uppercase_checkbox, 5, 0)
        layout.addWidget(self.lowercase_checkbox, 5, 1)
        layout.addWidget(self.digits_checkbox, 6, 0)
        layout.addWidget(self.symbols_checkbox, 6, 1)

        layout.addWidget(self.strength_label, 7, 0, 1, 3)
        layout.addWidget(self.strength_indicator, 7, 1, 1, 3)

        layout.addWidget(self.generate_button, 9, 0)
        layout.addWidget(self.reset_button, 9, 1)

        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

    def generate_password(self):
        password_length = self.length_slider.value()
        use_uppercase = self.uppercase_checkbox.isChecked()
        use_lowercase = self.lowercase_checkbox.isChecked()
        use_digits = self.digits_checkbox.isChecked()
        use_symbols = self.symbols_checkbox.isChecked()

        characters = ''
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            self.password_output.setText('Please select at least one character type.')
            return

        generated_password = ''.join(random.choice(characters) for _ in range(password_length))
        self.password_output.setText(generated_password)

        strength_score = self.calculate_strength(generated_password)
        self.update_strength_indicator(strength_score)

    def reset_password(self):
        self.password_output.clear()
        self.length_slider.setValue(12)
        self.uppercase_checkbox.setChecked(False)
        self.lowercase_checkbox.setChecked(False)
        self.digits_checkbox.setChecked(False)
        self.symbols_checkbox.setChecked(False)
        self.strength_indicator.clear()

    def calculate_strength(self, password):
        return len(password)

    def update_strength_indicator(self, strength_score):
        color = 'red' if strength_score < 8 else 'green'
        strength_text = 'Weak' if strength_score < 8 else 'Strong'

        self.strength_indicator.setText(strength_text)
        self.strength_indicator.setStyleSheet(f"QLabel {{ color: {color};font-weight: bold; }}")

    def style_smooth_checkbox(self, checkbox):
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                border-radius: 6px;
                border: 1px solid #000000;
            }
            QCheckBox::indicator:checked {
                background-color: #007AFF;
                border: 1px solid #000000;
            }
        """)

    def style_smooth_button(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
