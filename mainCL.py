import tkinter as tk


def add_to_display(value):
	display.insert(tk.END, value)


def clear_display():
	display.delete(0, tk.END)


def calculate():
	expression = display.get()
	if not expression or any(character not in "0123456789.+-*/() " for character in expression):
		return

	try:
		result = eval(expression, {"__builtins__": None}, {})
		clear_display()
		display.insert(0, str(result))
	except (ArithmeticError, SyntaxError, TypeError):
		clear_display()
		display.insert(0, "Error")


window = tk.Tk()
window.title("Simple Calculator")
window.geometry("320x430")
window.configure(bg="#202124")

display = tk.Entry(
	window,
	font=("Arial", 24),
	justify="right",
	bg="#303134",
	fg="white",
	insertbackground="white",
	borderwidth=0,
)
display.pack(fill="x", padx=16, pady=20, ipady=12)

buttons_frame = tk.Frame(window, bg="#202124")
buttons_frame.pack(expand=True, fill="both", padx=12, pady=8)

buttons = [
	("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
	("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
	("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
	("0", 3, 0), (".", 3, 1), ("C", 3, 2), ("+", 3, 3),
]

for text, row, column in buttons:
	command = clear_display if text == "C" else lambda value=text: add_to_display(value)
	tk.Button(
		buttons_frame,
		text=text,
		command=command,
		font=("Arial", 16, "bold"),
		bg="#3c4043" if text not in "+-*/C" else "#f29900",
		fg="white",
		activebackground="#5f6368",
		borderwidth=0,
	).grid(row=row, column=column, sticky="nsew", padx=4, pady=4)

for index in range(4):
	buttons_frame.columnconfigure(index, weight=1)
	buttons_frame.rowconfigure(index, weight=1)

tk.Button(
	buttons_frame,
	text="=",
	command=calculate,
	font=("Arial", 16, "bold"),
	bg="#1a73e8",
	fg="white",
	activebackground="#4285f4",
	borderwidth=0,
).grid(row=4, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)
buttons_frame.rowconfigure(4, weight=1)

window.mainloop()
