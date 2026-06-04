import customtkinter as ctk
import random

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Scores
user_score = 0
computer_score = 0

choices = ["Rock", "Paper", "Scissors"]

def play(user_choice):
    global user_score, computer_score

    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "🤝 It's a Tie!"
    elif (
        (user_choice == "Rock" and computer_choice == "Scissors")
        or (user_choice == "Paper" and computer_choice == "Rock")
        or (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        result = "🎉 You Win!"
        user_score += 1
    else:
        result = "💻 Computer Wins!"
        computer_score += 1

    user_choice_label.configure(text=f"Your Choice: {user_choice}")
    computer_choice_label.configure(text=f"Computer Choice: {computer_choice}")
    result_label.configure(text=result)

    score_label.configure(
        text=f"Player: {user_score}   |   Computer: {computer_score}"
    )

def reset_game():
    global user_score, computer_score

    user_score = 0
    computer_score = 0

    user_choice_label.configure(text="Your Choice:")
    computer_choice_label.configure(text="Computer Choice:")
    result_label.configure(text="Make your move!")
    score_label.configure(text="Player: 0 | Computer: 0")


app = ctk.CTk()
app.title("Rock Paper Scissors")
app.geometry("700x550")
app.resizable(False, False)

title = ctk.CTkLabel(
    app,
    text="✂️ Rock Paper Scissors",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)

instruction = ctk.CTkLabel(
    app,
    text="Choose one option below",
    font=("Arial", 16)
)
instruction.pack()

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=25)

rock_btn = ctk.CTkButton(
    button_frame,
    text="🪨 Rock",
    width=160,
    height=50,
    command=lambda: play("Rock")
)
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = ctk.CTkButton(
    button_frame,
    text="📄 Paper",
    width=160,
    height=50,
    command=lambda: play("Paper")
)
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = ctk.CTkButton(
    button_frame,
    text="✂️ Scissors",
    width=160,
    height=50,
    command=lambda: play("Scissors")
)
scissors_btn.grid(row=0, column=2, padx=10)

user_choice_label = ctk.CTkLabel(
    app,
    text="Your Choice:",
    font=("Arial", 18)
)
user_choice_label.pack(pady=10)

computer_choice_label = ctk.CTkLabel(
    app,
    text="Computer Choice:",
    font=("Arial", 18)
)
computer_choice_label.pack(pady=10)

result_label = ctk.CTkLabel(
    app,
    text="Make your move!",
    font=("Arial", 24, "bold")
)
result_label.pack(pady=20)

score_label = ctk.CTkLabel(
    app,
    text="Player: 0 | Computer: 0",
    font=("Arial", 20, "bold")
)
score_label.pack(pady=15)

reset_btn = ctk.CTkButton(
    app,
    text="🔄 Reset Game",
    width=200,
    height=45,
    command=reset_game
)
reset_btn.pack(pady=20)

app.mainloop()