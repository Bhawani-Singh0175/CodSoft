import customtkinter as ctk
from tkinter import messagebox

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        op = operation.get()

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero")
                return
            result = num1 / num2
        else:
            messagebox.showwarning("Warning", "Select an operation")
            return

        result_label.configure(text=f"Result: {result}")

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")


def clear():
    entry1.delete(0, "end")
    entry2.delete(0, "end")
    result_label.configure(text="Result:")
    operation.set("")


# Main Window
app = ctk.CTk()
app.title("Modern Calculator")
app.geometry("500x500")
app.resizable(False, False)

# Title
title = ctk.CTkLabel(
    app,
    text="🧮 Simple Calculator",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

# Number Inputs
entry1 = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter First Number"
)
entry1.pack(pady=10)

entry2 = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter Second Number"
)
entry2.pack(pady=10)

# Operation Selection
operation = ctk.StringVar(value="+")

frame = ctk.CTkFrame(app)
frame.pack(pady=20)

ctk.CTkRadioButton(frame, text="Add", variable=operation, value="+").grid(row=0, column=0, padx=10)
ctk.CTkRadioButton(frame, text="Subtract", variable=operation, value="-").grid(row=0, column=1, padx=10)
ctk.CTkRadioButton(frame, text="Multiply", variable=operation, value="*").grid(row=0, column=2, padx=10)
ctk.CTkRadioButton(frame, text="Divide", variable=operation, value="/").grid(row=0, column=3, padx=10)

# Buttons
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=20)

calculate_btn = ctk.CTkButton(
    btn_frame,
    text="Calculate",
    command=calculate,
    width=120,
    height=40
)
calculate_btn.grid(row=0, column=0, padx=10)

clear_btn = ctk.CTkButton(
    btn_frame,
    text="Clear",
    command=clear,
    width=120,
    height=40
)
clear_btn.grid(row=0, column=1, padx=10)

# Result
result_label = ctk.CTkLabel(
    app,
    text="Result:",
    font=("Arial", 22, "bold")
)
result_label.pack(pady=20)

app.mainloop()