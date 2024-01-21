import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random

class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Rock, Paper, Scissors')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('icon.png'))

        self.init_ui()

        self.player_wins = 0
        self.computer_wins = 0

    def init_ui(self):
        self.setStyleSheet("background-color: #F5F5F5;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.start_screen()

    def start_screen(self):
        start_label = QLabel('Rock, Paper, Scissors', self)
        start_label.setAlignment(Qt.AlignCenter)
        start_label.setStyleSheet("color: #007AFF; font-size: 32px; font-weight: bold; font-family: 'San Francisco'; margin-bottom: 20px;")

        start_button = QPushButton('Start Game', self)
        start_button.setStyleSheet("background-color: #007AFF; color: white; font-size: 24px; padding: 12px 24px; border-radius: 8px; font-family: 'San Francisco';")
        start_button.clicked.connect(self.game_screen)

        self.main_layout.addWidget(start_label)
        self.main_layout.addWidget(start_button)

    def game_screen(self):
        self.clear_layout()

        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #007AFF; font-size: 32px; font-weight: bold; margin-bottom: 20px; font-family: 'San Francisco';")

        self.player_label = QLabel('Your choice: ')
        self.player_label.setStyleSheet("color: #333333; font-size: 24px; margin-bottom: 15px; font-family: 'San Francisco';")

        self.computer_label = QLabel('Computer choice: ')
        self.computer_label.setStyleSheet("color: #333333; font-size: 24px; margin-bottom: 15px; font-family: 'San Francisco';")

        self.rock_button = QPushButton('Rock', self)
        self.paper_button = QPushButton('Paper', self)
        self.scissors_button = QPushButton('Scissors', self)

        button_style = "color: white; font-size: 24px; padding: 12px 24px; border-radius: 8px; margin-bottom: 15px; font-family: 'San Francisco';"
        self.rock_button.setStyleSheet(f"background-color: #007AFF; {button_style}")
        self.paper_button.setStyleSheet(f"background-color: #007AFF; {button_style}")
        self.scissors_button.setStyleSheet(f"background-color: #007AFF; {button_style}")

        self.rock_button.clicked.connect(lambda: self.play_game('Rock'))
        self.paper_button.clicked.connect(lambda: self.play_game('Paper'))
        self.scissors_button.clicked.connect(lambda: self.play_game('Scissors'))

        reset_button = QPushButton('Reset Game', self)
        reset_button.setStyleSheet("background-color: #FF3B30; color: white; font-size: 24px; padding: 12px 24px; border-radius: 8px; margin-bottom: 20px; font-family: 'San Francisco';")
        reset_button.clicked.connect(self.reset_game)

        self.main_layout.addWidget(self.result_label)
        self.main_layout.addWidget(self.player_label)
        self.main_layout.addWidget(self.computer_label)
        self.main_layout.addWidget(self.rock_button)
        self.main_layout.addWidget(self.paper_button)
        self.main_layout.addWidget(self.scissors_button)
        self.main_layout.addWidget(reset_button)

        self.update_scoreboard()

    def play_game(self, player_choice):
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)

        self.player_label.setText(f'Your choice: {player_choice}')
        self.computer_label.setText(f'Computer choice: {computer_choice}')

        self.determine_winner(player_choice, computer_choice)

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            result = 'It\'s a tie!'
        elif (
            (player_choice == 'Rock' and computer_choice == 'Scissors') or
            (player_choice == 'Paper' and computer_choice == 'Rock') or
            (player_choice == 'Scissors' and computer_choice == 'Paper')
        ):
            result = 'You win!'
            self.player_wins += 1
        else:
            result = 'You lose!'
            self.computer_wins += 1

        self.result_label.setText(result)
        self.update_scoreboard()

    def update_scoreboard(self):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if isinstance(item.widget(), QLabel) and "Score:" in item.widget().text():
                item.widget().setParent(None)

        score_text = f'Score: {self.player_wins} - {self.computer_wins}'
        score_label = QLabel(score_text, self)
        score_label.setStyleSheet("color: #333333; font-size: 18px; font-family: 'San Francisco'; margin-bottom: 20px;")
        self.main_layout.addWidget(score_label)

    def reset_game(self):
        self.clear_layout()
        self.player_wins = 0
        self.computer_wins = 0
        self.start_screen()

    def clear_layout(self):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)

            if item.widget():
                item.widget().setParent(None)
            elif item.spacerItem():
                self.main_layout.removeItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())
