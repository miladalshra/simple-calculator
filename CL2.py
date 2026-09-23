"""A modern, safe scientific calculator with no external dependencies."""

from __future__ import annotations

import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox, ttk


class SafeCalculator:
	"""Evaluates only the arithmetic syntax and functions exposed here."""

	FUNCTIONS = {
		"sin": math.sin,
		"cos": math.cos,
		"tan": math.tan,
		"asin": math.asin,
		"acos": math.acos,
		"atan": math.atan,
		"sqrt": math.sqrt,
		"log": math.log10,
		"ln": math.log,
		"abs": abs,
		"floor": math.floor,
		"ceil": math.ceil,
		"factorial": math.factorial,
	}
	CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}
	BINARY_OPERATORS = {
		ast.Add: operator.add,
		ast.Sub: operator.sub,
		ast.Mult: operator.mul,
		ast.Div: operator.truediv,
		ast.Pow: operator.pow,
		ast.Mod: operator.mod,
		ast.FloorDiv: operator.floordiv,
	}
	UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

	def evaluate(self, expression: str, degrees: bool = False) -> float:
		tree = ast.parse(expression, mode="eval")

		def visit(node: ast.AST) -> float:
			if isinstance(node, ast.Expression):
				return visit(node.body)
			if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
				return node.value
			if isinstance(node, ast.Name) and node.id in self.CONSTANTS:
				return self.CONSTANTS[node.id]
			if isinstance(node, ast.BinOp) and type(node.op) in self.BINARY_OPERATORS:
				return self.BINARY_OPERATORS[type(node.op)](visit(node.left), visit(node.right))
			if isinstance(node, ast.UnaryOp) and type(node.op) in self.UNARY_OPERATORS:
				return self.UNARY_OPERATORS[type(node.op)](visit(node.operand))
			if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
				function = self.FUNCTIONS.get(node.func.id)
				if function is None or node.keywords or len(node.args) > 2:
					raise ValueError("Function not allowed")
				args = [visit(argument) for argument in node.args]
				if degrees and node.func.id in {"sin", "cos", "tan"}:
					args[0] = math.radians(args[0])
				result = function(*args)
				return result
			raise ValueError("Expression not allowed")

		result = visit(tree)
		if not math.isfinite(result):
			raise ValueError("Result is not finite")
		return result


class CalculatorApp:
	COLORS = {
		"background": "#111827",
		"panel": "#1f2937",
		"display": "#0b1220",
		"button": "#263449",
		"button_hover": "#34465f",
		"operator": "#d97706",
		"accent": "#14b8a6",
		"text": "#f8fafc",
		"muted": "#94a3b8",
	}

	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Scientific Calculator")
		self.root.geometry("760x620")
		self.root.minsize(650, 520)
		self.root.configure(bg=self.COLORS["background"])
		self.engine = SafeCalculator()
		self.expression = tk.StringVar()
		self.result_text = tk.StringVar(value="Ready")
		self.memory = 0.0
		self.degrees = tk.BooleanVar(value=False)
		self.history: list[tuple[str, str]] = []
		self._build_style()
		self._build_ui()
		self.root.bind("<Return>", lambda _event: self.calculate())
		self.root.bind("<KP_Enter>", lambda _event: self.calculate())
		self.root.bind("<Escape>", lambda _event: self.clear())

	def _build_style(self):
		style = ttk.Style(self.root)
		style.theme_use("clam")
		style.configure("TFrame", background=self.COLORS["background"])
		style.configure("Panel.TFrame", background=self.COLORS["panel"])
		style.configure("TLabel", background=self.COLORS["background"], foreground=self.COLORS["text"])
		style.configure("Panel.TLabel", background=self.COLORS["panel"], foreground=self.COLORS["text"])
		style.configure("Muted.TLabel", background=self.COLORS["panel"], foreground=self.COLORS["muted"])
		style.configure("TCheckbutton", background=self.COLORS["panel"], foreground=self.COLORS["text"])
		style.configure("Treeview", background=self.COLORS["display"], fieldbackground=self.COLORS["display"], foreground=self.COLORS["text"], rowheight=28)
		style.configure("Treeview.Heading", background=self.COLORS["button"], foreground=self.COLORS["text"])

	def _build_ui(self):
		header = ttk.Frame(self.root, padding=(24, 18))
		header.pack(fill="x")
		ttk.Label(header, text="Scientific Calculator", font=("Segoe UI", 22, "bold")).pack(side="left")
		ttk.Label(header, text="Fast, accurate, and safe calculations", style="Muted.TLabel", font=("Segoe UI", 10)).pack(side="left", padx=16, pady=(8, 0))

		content = ttk.Frame(self.root)
		content.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		content.columnconfigure(0, weight=3)
		content.columnconfigure(1, weight=2)
		content.rowconfigure(0, weight=1)

		calculator = ttk.Frame(content, style="Panel.TFrame", padding=16)
		calculator.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
		calculator.columnconfigure(0, weight=1)
		calculator.rowconfigure(3, weight=1)

		display_frame = tk.Frame(calculator, bg=self.COLORS["display"], padx=14, pady=10)
		display_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
		tk.Label(display_frame, textvariable=self.result_text, bg=self.COLORS["display"], fg=self.COLORS["muted"], font=("Segoe UI", 10), anchor="e").pack(fill="x")
		tk.Entry(display_frame, textvariable=self.expression, bg=self.COLORS["display"], fg=self.COLORS["text"], insertbackground=self.COLORS["accent"], relief="flat", justify="right", font=("Segoe UI", 25, "bold")).pack(fill="x", ipady=8)

		options = ttk.Frame(calculator, style="Panel.TFrame")
		options.grid(row=1, column=0, sticky="ew", pady=(0, 10))
		ttk.Checkbutton(options, text="Degrees (DEG)", variable=self.degrees).pack(side="left")
		ttk.Label(options, text="Functions: sin  cos  tan  sqrt  log  ln", style="Muted.TLabel").pack(side="right")

		buttons = [
			[("MC", "memory_clear"), ("MR", "memory_recall"), ("M+", "memory_add"), ("M-", "memory_sub"), ("Clear", "clear")],
			[("sin", "insert"), ("cos", "insert"), ("tan", "insert"), ("log", "insert"), ("ln", "insert")],
			[("7", "insert"), ("8", "insert"), ("9", "insert"), ("/", "insert"), ("(", "insert")],
			[("4", "insert"), ("5", "insert"), ("6", "insert"), ("*", "insert"), (")", "insert")],
			[("1", "insert"), ("2", "insert"), ("3", "insert"), ("-", "insert"), ("^", "insert")],
			[("0", "insert"), (".", "insert"), ("pi", "insert"), ("+", "insert"), ("=", "calculate")],
		]
		grid = ttk.Frame(calculator, style="Panel.TFrame")
		grid.grid(row=3, column=0, sticky="nsew")
		for row_index, row in enumerate(buttons):
			grid.rowconfigure(row_index, weight=1)
			for column_index in range(5):
				grid.columnconfigure(column_index, weight=1)
			for column_index, (label, action) in enumerate(row):
				self._make_button(grid, label, action, row_index, column_index)

		history_panel = ttk.Frame(content, style="Panel.TFrame", padding=14)
		history_panel.grid(row=0, column=1, sticky="nsew")
		history_panel.rowconfigure(1, weight=1)
		history_panel.columnconfigure(0, weight=1)
		ttk.Label(history_panel, text="Calculation History", style="Panel.TLabel", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 12))
		self.history_view = ttk.Treeview(history_panel, columns=("expression", "result"), show="headings")
		self.history_view.heading("expression", text="Expression")
		self.history_view.heading("result", text="Result")
		self.history_view.column("expression", width=130, anchor="e")
		self.history_view.column("result", width=100, anchor="e")
		self.history_view.grid(row=1, column=0, sticky="nsew")
		self.history_view.bind("<Double-1>", self.use_history)
		ttk.Button(history_panel, text="Clear History", command=self.clear_history).grid(row=2, column=0, sticky="ew", pady=(12, 0))

		ttk.Label(self.root, text="Developed by Milad", style="Muted.TLabel", font=("Segoe UI", 9)).pack(side="bottom", pady=(0, 8))

	def _make_button(self, parent, label, action, row, column):
		is_operator = label in {"/", "*", "-", "+", "^", "="} or action == "clear"
		background = self.COLORS["accent"] if label == "=" else self.COLORS["operator"] if is_operator else self.COLORS["button"]
		button = tk.Button(parent, text=label, command=lambda: self._dispatch(action, label), bg=background, fg=self.COLORS["text"], activebackground=self.COLORS["button_hover"], activeforeground=self.COLORS["text"], relief="flat", bd=0, font=("Segoe UI", 13, "bold"), cursor="hand2")
		button.grid(row=row, column=column, sticky="nsew", padx=3, pady=3, ipadx=4, ipady=5)

	def _dispatch(self, action, label):
		if action == "insert":
			values = {"^": "**"}
			value = values.get(label, label)
			if label in {"sin", "cos", "tan", "log", "ln"}:
				value += "("
			self.expression.set(self.expression.get() + value)
		else:
			getattr(self, action)()

	def calculate(self):
		expression = self.expression.get().strip()
		if not expression:
			return
		try:
			value = self.engine.evaluate(expression, self.degrees.get())
			formatted = self._format(value)
			self.result_text.set("= " + formatted)
			self.history.insert(0, (expression, formatted))
			self.history_view.insert("", 0, values=(expression, formatted))
		except (ValueError, SyntaxError, TypeError, ArithmeticError, OverflowError):
			self.result_text.set("Error: check the expression")

	@staticmethod
	def _format(value):
		return f"{value:.12g}" if isinstance(value, float) else str(value)

	def clear(self):
		self.expression.set("")
		self.result_text.set("Ready")

	def memory_clear(self):
		self.memory = 0.0

	def memory_recall(self):
		self.expression.set(self.expression.get() + self._format(self.memory))

	def memory_add(self):
		self.memory += self.engine.evaluate(self.expression.get(), self.degrees.get())

	def memory_sub(self):
		self.memory -= self.engine.evaluate(self.expression.get(), self.degrees.get())

	def clear_history(self):
		self.history.clear()
		for item in self.history_view.get_children():
			self.history_view.delete(item)

	def use_history(self, _event):
		selection = self.history_view.selection()
		if selection:
			self.expression.set(self.history_view.item(selection[0], "values")[0])


def run_self_test():
	calculator = SafeCalculator()
	assert calculator.evaluate("2 + 3 * 4") == 14
	assert round(calculator.evaluate("sin(90)", degrees=True), 8) == 1
	assert calculator.evaluate("sqrt(81) + factorial(5)") == 129


if __name__ == "__main__":
	import sys

	if "--test" in sys.argv:
		run_self_test()
		print("All calculator tests passed")
	else:
		root = tk.Tk()
		CalculatorApp(root)
		root.mainloop()
