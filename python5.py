#!/usr/bin/env python3
"""
Tkinter Graphical Calculator
- Single-file Python 3 app using tkinter
- Safe expression evaluation using `ast` (no `eval` on raw input)
- Features: + - * / % ** parentheses, unary +/-, decimal numbers
- Keyboard support, Clear (C), Backspace (⌫), Copy result
- History panel (last 10 calculations)

Run: python tkinter_calculator.py
"""

import ast
import operator as op
import math
import tkinter as tk
from tkinter import ttk
from typing import Any

# Allowed operators mapping for AST evaluation
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed math functions
_ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,      # natural log
    'log10': math.log10,
    'abs': abs,
    'round': round,
}


def safe_eval_expr(expr: str) -> Any:
    """Safely evaluate a numeric expression using ast.
    Supported: numbers, binary ops (+ - * / % **), unary +/-, parentheses, and a small set of functions.
    Raises ValueError for unsupported expressions.
    """

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # < Py3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Py3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant: {node.value}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in _ALLOWED_FUNCTIONS:
                    args = [_eval(a) for a in node.args]
                    return _ALLOWED_FUNCTIONS[func_name](*args)
            raise ValueError("Unsupported function call")
        elif isinstance(node, ast.Name):
            # allow constants like 'pi' or 'e'
            if node.id == 'pi':
                return math.pi
            if node.id == 'e':
                return math.e
            raise ValueError(f"Unsupported identifier: {node.id}")
        elif isinstance(node, ast.Expr):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression: {type(node)}")

    try:
        parsed = ast.parse(expr, mode='eval')
        return _eval(parsed)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter Calculator')
        self.resizable(False, False)
        self.configure(padx=10, pady=10)

        # Styles
        style = ttk.Style(self)
        style.theme_use('default')

        # Display
        self.display_var = tk.StringVar()
        self.result_shown = False

        display_frame = ttk.Frame(self)
        display_frame.grid(row=0, column=0, sticky='nsew')

        self.entry = ttk.Entry(display_frame, textvariable=self.display_var, font=('Consolas', 18), justify='right', width=24)
        self.entry.grid(row=0, column=0, sticky='ew', padx=(0, 4), pady=(0, 6))
        self.entry.focus_set()

        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=1, column=0)

        btns = [
            ('C', 1, 0), ('⌫', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
        ]

        for (text, r, c) in btns:
            cmd = (lambda t=text: self.on_button_click(t))
            b = ttk.Button(buttons_frame, text=text, command=cmd, width=6)
            b.grid(row=r, column=c, padx=2, pady=2)

        # Extra functions frame
        funcs_frame = ttk.Frame(self)
        funcs_frame.grid(row=0, column=1, rowspan=2, padx=(8, 0), sticky='n')

        ttk.Button(funcs_frame, text='(', width=6, command=lambda: self.insert_text('(')).grid(row=0, column=0, pady=2)
        ttk.Button(funcs_frame, text=')', width=6, command=lambda: self.insert_text(')')).grid(row=1, column=0, pady=2)
        ttk.Button(funcs_frame, text='x²', width=6, command=lambda: self.insert_text('**2')).grid(row=2, column=0, pady=2)
        ttk.Button(funcs_frame, text='x³', width=6, command=lambda: self.insert_text('**3')).grid(row=3, column=0, pady=2)
        ttk.Button(funcs_frame, text='sqrt', width=6, command=lambda: self.insert_text('sqrt(')).grid(row=4, column=0, pady=2)
        ttk.Button(funcs_frame, text='pi', width=6, command=lambda: self.insert_text('pi')).grid(row=5, column=0, pady=2)
        ttk.Button(funcs_frame, text='Ans', width=6, command=self.insert_last_answer).grid(row=6, column=0, pady=2)
        ttk.Button(funcs_frame, text='Copy', width=6, command=self.copy_result).grid(row=7, column=0, pady=2)

        # History listbox
        history_frame = ttk.Frame(self)
        history_frame.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky='ew')
        ttk.Label(history_frame, text='History (click to reuse)').grid(row=0, column=0, sticky='w')
        self.history_list = tk.Listbox(history_frame, height=6)
        self.history_list.grid(row=1, column=0, sticky='ew')
        self.history_list.bind('<<ListboxSelect>>', self.on_history_select)

        self.history = []  # store tuples (expr, result)
        self.last_answer = ''

        # Key bindings
        self.bind_all('<Return>', lambda e: self.evaluate())
        self.bind_all('<BackSpace>', lambda e: self.backspace())
        self.bind_all('<Escape>', lambda e: self.clear())
        for key in '0123456789.+-*/()%':
            self.bind_all(key, lambda e, k=key: self.insert_text(k))

    def insert_text(self, txt: str):
        if self.result_shown:
            # if last action showed result and user types a number or '(' start fresh
            if txt.isdigit() or txt == '(' or txt == '.':
                self.display_var.set(txt)
                self.result_shown = False
                return
        pos = self.entry.index(tk.INSERT)
        cur = self.display_var.get()
        new = cur[:pos] + txt + cur[pos:]
        self.display_var.set(new)
        # move cursor after inserted text
        self.entry.icursor(pos + len(txt))

    def on_button_click(self, key: str):
        if key == 'C':
            self.clear()
        elif key == '⌫':
            self.backspace()
        elif key == '=':
            self.evaluate()
        elif key == '±':
            self.toggle_sign()
        else:
            self.insert_text(key)

    def clear(self):
        self.display_var.set('')
        self.result_shown = False

    def backspace(self):
        s = self.display_var.get()
        pos = self.entry.index(tk.INSERT)
        if pos > 0:
            new = s[:pos-1] + s[pos:]
            self.display_var.set(new)
            self.entry.icursor(pos-1)

    def toggle_sign(self):
        s = self.display_var.get()
        if not s:
            return
        try:
            # Try to find last number and toggle its sign
            # we'll simply evaluate and negate if it's the whole expression
            val = safe_eval_expr(s)
            self.display_var.set(str(-val))
            self.result_shown = True
        except Exception:
            # fallback: insert a leading '-(' and trailing ')' if helpful
            self.insert_text('(-')

    def insert_last_answer(self):
        if self.last_answer:
            self.insert_text(str(self.last_answer))

    def copy_result(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.last_answer)
        except Exception:
            pass

    def evaluate(self):
        expr = self.display_var.get().strip()
        if not expr:
            return
        try:
            result = safe_eval_expr(expr)
            # Format result: drop trailing .0 for ints
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display_var.set(str(result))
            self.result_shown = True
            # store history
            self.last_answer = str(result)
            self._add_history(expr, str(result))
        except Exception as e:
            self.display_var.set('Error')
            self.result_shown = True

    def _add_history(self, expr: str, result: str):
        entry = f"{expr} = {result}"
        # avoid duplicates and keep max 50 entries
        if self.history and self.history[-1] == entry:
            return
        self.history.append(entry)
        if len(self.history) > 50:
            self.history.pop(0)
        # update listbox with last 10
        self.history_list.delete(0, tk.END)
        for itm in reversed(self.history[-10:]):
            self.history_list.insert(tk.END, itm)

    def on_history_select(self, event):
        sel = event.widget.curselection()
        if not sel:
            return
        idx = sel[0]
        text = event.widget.get(idx)
        # text format: "expr = result"
        if ' = ' in text:
            expr, _ = text.split(' = ', 1)
            self.display_var.set(expr)


if __name__ == '__main__':
    app = Calculator()
    app.mainloop()
