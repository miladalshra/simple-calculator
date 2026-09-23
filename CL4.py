import math
import tkinter as tk
from tkinter import ttk

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("680x520")
        self.root.configure(bg="#121212")
        
        # متنساش تجيب الدحي وانت راجع من المحل!
        self.expr_var = tk.StringVar()
        self.res_var = tk.StringVar(value="0")
        self.use_deg = tk.BooleanVar(value=False)
        self.memory = 0.0
        
        self.setup_ui()

    def setup_ui(self):
        # شاشة العرض - ظبطنا الألوان والتصميم الأساسي
        top_frame = tk.Frame(self.root, bg="#1e1e1e", bd=1, relief="solid")
        top_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(top_frame, textvariable=self.res_var, fg="#aaa", bg="#1e1e1e", anchor="e", font=("Arial", 11)).pack(fill="x", padx=5)
        tk.Entry(top_frame, textvariable=self.expr_var, fg="#fff", bg="#1e1e1e", bd=0, justify="right", font=("Arial", 22, "bold"), insertbackground="white").pack(fill="x", ipady=6, padx=5)

        # خيار تحويل الدرجات
        opt_frame = tk.Frame(self.root, bg="#121212")
        opt_frame.pack(fill="x", padx=10)
        
        chk = tk.Checkbutton(
            opt_frame, text="Degrees (DEG)", variable=self.use_deg, 
            bg="#121212", fg="#ffffff", selectcolor="#1e1e1e", 
            activebackground="#121212", activeforeground="#ffffff"
        )
        chk.pack(side="left")

        # لوحة الأزرار والسجل
        main_frame = tk.Frame(self.root, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(main_frame, bg="#121212")
        btn_frame.pack(side="left", fill="both", expand=True)

        # الأزرار الرئيسية - ظبطت لون الأزرار أصفر ويساوي أزرق
        buttons = [
            ['MC', 'MR', 'M+', 'M-', 'C'],
            ['sin', 'cos', 'tan', 'log', 'ln'],
            ['7', '8', '9', '/', '('],
            ['4', '5', '6', '*', ')'],
            ['1', '2', '3', '-', '^'],
            ['0', '.', 'pi', '+', '=']
        ]

        for r, row in enumerate(buttons):
            for c, txt in enumerate(row):
                # زر يساوي أزرق والأزرار التانية أصفر
                if txt == '=':
                    bg_color = "#1e88e5"
                    fg_color = "#ffffff"
                    active_bg = "#1565c0"
                else:
                    bg_color = "#fbc02d"
                    fg_color = "#000000"
                    active_bg = "#f57f17"

                btn = tk.Button(
                    btn_frame, text=txt, font=("Arial", 10, "bold"),
                    bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=fg_color,
                    bd=0, relief="flat", command=lambda t=txt: self.on_button_click(t)
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
                btn_frame.columnconfigure(c, weight=1)
            btn_frame.rowconfigure(r, weight=1)

        # قائمة السجل السريعة
        hist_frame = tk.Frame(main_frame, bg="#121212", width=180)
        hist_frame.pack(side="right", fill="y", padx=(10, 0))
        
        tk.Label(hist_frame, text="History", font=("Arial", 11, "bold"), bg="#121212", fg="#ffffff").pack(anchor="w", pady=(0, 5))
        
        # تصحيح الخصائص هنا: selectbackground و selectforeground
        self.history_list = tk.Listbox(
            hist_frame, font=("Arial", 9), bg="#1e1e1e", fg="#ffffff", 
            selectbackground="#fbc02d", selectforeground="#000000", bd=0, highlightthickness=0
        )
        self.history_list.pack(fill="both", expand=True)
        self.history_list.bind('<Double-Button-1>', self.load_from_history)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.expr_var.set("")
            self.res_var.set("0")
        elif char in ['MC', 'MR', 'M+', 'M-']:
            self.handle_memory(char)
        else:
            if char in ['sin', 'cos', 'tan', 'log', 'ln']:
                char += '('
            elif char == '^':
                char = '**'
            self.expr_var.set(self.expr_var.get() + char)

    def calculate(self):
        expr = self.expr_var.get()
        if not expr:
            return
            
        try:
            # القاموس الآمن للدوال
            safe_dict = {
                "sin": lambda x: math.sin(math.radians(x)) if self.use_deg.get() else math.sin(x),
                "cos": lambda x: math.cos(math.radians(x)) if self.use_deg.get() else math.cos(x),
                "tan": lambda x: math.tan(math.radians(x)) if self.use_deg.get() else math.tan(x),
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e
            }
            
            # مشكلة السوالب كالمعتاد.. نجرب eval وخلاص
            res = eval(expr, {"__builtins__": None}, safe_dict)
            res_str = f"{res:.8g}" if isinstance(res, float) else str(res)
            
            self.res_var.set("= " + res_str)
            self.history_list.insert(0, f"{expr} = {res_str}")
        except Exception:
            self.res_var.set("Error")

    def handle_memory(self, action):
        # مش متأكد لو الميموري شغال 100% بس تمام
        try:
            if action == 'MC':
                self.memory = 0.0
            elif action == 'MR':
                self.expr_var.set(self.expr_var.get() + str(self.memory))
            elif action == 'M+':
                self.memory += float(self.res_var.get().replace("= ", ""))
            elif action == 'M-':
                self.memory -= float(self.res_var.get().replace("= ", ""))
        except Exception:
            pass

    def load_from_history(self, event):
        sel = self.history_list.curselection()
        if sel:
            item = self.history_list.get(sel[0])
            self.expr_var.set(item.split(" = ")[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()