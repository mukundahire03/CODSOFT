import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissorsGame:
    def __init__(self):
        self.user_score = 0
        self.computer_score = 0

        self.window = tk.Tk()
        self.window.title("Rock, Paper, Scissors Game")

        self.user_choice_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.score_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Choose rock, paper, or scissors:", font=("Helvetica", 12)).pack(pady=10)

        choices = ['rock', 'paper', 'scissors']
        for choice in choices:
            tk.Radiobutton(self.window, text=choice.capitalize(), variable=self.user_choice_var, value=choice, font=("Helvetica", 10)).pack()

        tk.Button(self.window, text="Play", command=self.play_game, font=("Helvetica", 12)).pack(pady=10)
        tk.Label(self.window, textvariable=self.result_var, font=("Helvetica", 12)).pack(pady=10)
        tk.Label(self.window, textvariable=self.score_var, font=("Helvetica", 12)).pack(pady=10)

    def play_game(self):
        user_choice = self.user_choice_var.get()
        computer_choice = random.choice(['rock', 'paper', 'scissors'])

        result = self.determine_winner(user_choice, computer_choice)
        self.display_result(user_choice, computer_choice, result)

        if 'win' in result:
            self.user_score += 1
        elif 'lose' in result:
            self.computer_score += 1

        self.update_score()

        # Show feedback in a pop-up window
        messagebox.showinfo("Result", f"You chose {user_choice.capitalize()}.\nThe computer chose {computer_choice.capitalize()}.\n{result}")

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'scissors' and computer_choice == 'paper') or \
             (user_choice == 'paper' and computer_choice == 'rock'):
            return "You win!"
        else:
            return "You lose!"

    def display_result(self, user_choice, computer_choice, result):
        self.result_var.set(f"Result: You chose {user_choice.capitalize()}. Computer chose {computer_choice.capitalize()}. {result}")

    def update_score(self):
        self.score_var.set(f"Score - You: {self.user_score}, Computer: {self.computer_score}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
