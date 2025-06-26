import tkinter as tk
import math
import os

# ================================
# Layouts for calculator modes
# ================================
simple_buttons = [
    ["AC", "⌫", "%", "+"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "÷"],
    ["⇋", "0", ".", "🟰"]
]

scientific_buttons = [
    ["deg/rad", "sin", "cos", "tan", "AC", "⌫"],
    ["sin⁻¹", "cos⁻¹", "tan⁻¹", "log", "ln", "%"],
    ["7", "8", "9", "√", "x⁻¹", "+"],
    ["4", "5", "6", "ⁿ√", "x²", "-"],
    ["1", "2", "3", "!", "x³", "×"],
    ["0", ".", "π", "e", "xⁿ", "÷"],
    ["⇋", "[", "]", "(", ")", "🟰"]
]

# ================================
# Global states
# ================================
mode = "deg"
calc_mode = "simple"
history = []
special_buttons = {}
button_widgets = []

# ================================
# Math functions
# ================================
functions = {
    "sin": lambda x: math.sin(math.radians(x)) if mode == "deg" else math.sin(x),
    "cos": lambda x: math.cos(math.radians(x)) if mode == "deg" else math.cos(x),
    "tan": lambda x: math.tan(math.radians(x)) if mode == "deg" else math.tan(x),
    "sin⁻¹": lambda x: math.degrees(math.asin(x)) if mode == "deg" else math.asin(x),
    "cos⁻¹": lambda x: math.degrees(math.acos(x)) if mode == "deg" else math.acos(x),
    "tan⁻¹": lambda x: math.degrees(math.atan(x)) if mode == "deg" else math.atan(x),
    "log": math.log10,
    "ln": math.log,
    "√": math.sqrt,
    "x²": lambda x: x**2,
    "x³": lambda x: x**3,
    "!": math.factorial,
    "x⁻¹": lambda x: 1 / x if x != 0 else float('inf'),
}

# ================================
# Button logic
# ================================
def click(event):
    global calc_mode
    text = event.widget.cget("text")
    current = entry.get()

    if text == "deg/rad":
        toggle_mode()
        return
    elif text == "⇋":
        calc_mode = "simple" if calc_mode == "scientific" else "scientific"
        draw_buttons()
        return
    elif text == "🟰":
        try:
            safe_expr = current.replace('🟰','=').replace('÷','/').replace('×','*').replace('xⁿ', '**').replace('[', '(').replace(']', ')').replace('%', '/100')
            if "ⁿ√" in safe_expr:
                base, n = safe_expr.split("ⁿ√")
                result = float(n) ** (1 / float(base))
            else:
                result = eval(safe_expr)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
            history.append(current + " = " + str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "AC":
        entry.delete(0, tk.END)
    elif text == "⌫":
        entry.delete(len(current)-1, tk.END)
    elif text in functions:
        try:
            value = eval(current)
            result = functions[text](value)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
            history.append(f"{text}({value}) = {result}")
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "π":
        entry.insert(tk.END, str(math.pi))
    elif text == "e":
        entry.insert(tk.END, str(math.e))
    else:
        entry.insert(tk.END, text)

# ================================
# Toggle Degree/Radian
# ================================
def toggle_mode():
    global mode
    mode = "rad" if mode == "deg" else "deg"
    if "mode_label" in special_buttons:
        special_buttons["mode_label"].config(text=f"Mode: {mode}")

# ================================
# Draw calculator buttons (DARK MODE)
# ================================
def draw_buttons():
    global button_widgets
    for btn in button_widgets:
        btn.destroy()
    button_widgets.clear()

    buttons = scientific_buttons if calc_mode == "scientific" else simple_buttons

    for i, row in enumerate(buttons):
        for j, btn_text in enumerate(row):
            if btn_text == "deg/rad":
                frame = tk.Frame(root, relief=tk.RAISED, bd=5, bg="#2e2e2e")
                frame.grid(row=i+3, column=j, sticky="nsew", padx=2, pady=2)
                mode_label = tk.Label(frame, text=f"Mode: {mode}", font="Arial 10", bg="#2e2e2e", fg="white")
                mode_label.pack(expand=True)
                deg_rad_button = tk.Button(frame, text=btn_text, font="Arial 14", padx=14, pady=18,
                                           relief=tk.RAISED, bd=5, bg="#2e2e2e", fg="white", activebackground="#3a3a3a")
                deg_rad_button.pack(expand=True)
                deg_rad_button.bind("<ButtonPress-1>", on_press)
                deg_rad_button.bind("<ButtonRelease-1>", on_release)
                special_buttons["deg_rad_button"] = deg_rad_button
                special_buttons["mode_label"] = mode_label
                button_widgets.append(frame)
            else:
                color = "#2e2e2e"
                fg = "white"
                font_size = 14

                if btn_text == "⇋":
                    color = "#3a8fb7"
                    font_size = 18
                elif btn_text in ["+", "-", "×", "÷", "%", "!", "x⁻¹", "x³", "x²", "√", "xⁿ", "e", "π", "ⁿ√"]:
                    fg = "yellow"
                elif btn_text in ["sin", "cos", "tan", "sin⁻¹", "cos⁻¹", "tan⁻¹", "log", "ln"]:
                    fg = "#7ec850"
                elif btn_text in ["AC", "⌫"]:
                    color = "#A0522D"
                    font_size = 18
                elif btn_text in ["(", ")", "[", "]"]:
                    fg = "#d19a66"
                elif btn_text == "=" or btn_text == "🟰":
                    font_size = 18
                    color = "#CB693C"
                elif btn_text in [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    font_size = 16

                btn = tk.Button(root, text=btn_text, font=f"Arial {font_size}", padx=14, pady=18,
                                relief=tk.RAISED, bd=5, bg=color, fg=fg,
                                activebackground="#3a3a3a", activeforeground="white")
                btn.grid(row=i+3, column=j, sticky="nsew", padx=2, pady=2)
                btn.bind("<ButtonPress-1>", on_press)
                btn.bind("<ButtonRelease-1>", on_release)
                button_widgets.append(btn)

    for btn in button_widgets:
        if isinstance(btn, tk.Button) and btn.cget("text") == "🟰":
            btn.config(bg="#0DB431", activebackground="#009f20", activeforeground="white")
        elif isinstance(btn, tk.Button) and btn.cget("text") == "⌫":
            btn.config(bg="#A0522D", activebackground="#713418")
        elif isinstance(btn, tk.Button) and btn.cget("text") == "AC":
            btn.config(bg="#A0522D", activebackground="#713418",activeforeground="red")
        elif isinstance(btn, tk.Button) and btn.cget("text") == ".":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "0":
            btn.config( activeforeground="#00bfff", ) 
        elif isinstance(btn, tk.Button) and btn.cget("text") == "1":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "2":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "3":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "4":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "5":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "6":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "7":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "8":
            btn.config( activeforeground="#00bfff", )
        elif isinstance(btn, tk.Button) and btn.cget("text") == "9":
            btn.config( activeforeground="#00bfff", )

# ================================
# History functions
# ================================
def show_history_frame():
    entry.grid_remove()
    for btn in button_widgets:
        btn.grid_remove()
    history_button.grid_remove()

    history_frame.grid(row=0, column=0, columnspan=8, rowspan=10, sticky="nsew")
    history_text.config(state=tk.NORMAL)
    history_text.delete("1.0", tk.END)
    for item in reversed(history[-100:]):
        history_text.insert(tk.END, item + "\n")
    history_text.config(state=tk.DISABLED)

def hide_history_frame():
    history_frame.grid_remove()
    entry.grid()
    history_button_frame.grid()
    for btn in button_widgets:
        btn.grid()

def clear_history():
    history.clear()
    history_text.config(state=tk.NORMAL)
    history_text.delete("1.0", tk.END)
    history_text.config(state=tk.DISABLED)
    save_history()

# ================================
# Button Events
# ================================
def on_press(e):
    e.widget.config(relief=tk.SUNKEN)

def on_release(e):
    e.widget.config(relief=tk.RAISED)
    click(e)



# ================================
# History File Handling
# ================================
HISTORY_FILE = "calc_history.txt"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                history.append(line.strip())

def save_history():
    with open(HISTORY_FILE, "w") as f:
        for item in history:
            f.write(item + "\n")

# ================================
# GUI setup
# ================================
root = tk.Tk()
root.title("Ultimate Scientific Calculator")
root.configure(bg="#1e1e1e")

for i in range(8):
    root.grid_columnconfigure(i, weight=1)
for i in range(10):
    root.grid_rowconfigure(i, weight=1)

entry = tk.Entry(root, font="Arial 20", bd=10, relief=tk.RIDGE, justify=tk.RIGHT,
                 bg="#2e2e2e", fg="white", insertbackground="white")
entry.grid(row=0, column=0, columnspan=8, ipadx=8, ipady=15, sticky="nsew", padx=2, pady=2)

# Frame to create yellow border
history_button_frame = tk.Frame(root, bg="yellow", bd=0)
history_button_frame.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=2, pady=2)

# Actual HISTORY button inside the frame
history_button = tk.Button(history_button_frame,
                           text="HISTORY",
                           font="Arial 12 bold",
                           bg="#1e1e1e",
                           fg="white",
                           activebackground="#7C7874",
                           activeforeground="white",
                           command=show_history_frame,
                           relief=tk.FLAT)
history_button.pack(fill="both", expand=True, padx=2, pady=2)

history_frame = tk.Frame(root, bg="#1e1e1e")
history_frame.grid_columnconfigure(0, weight=1)
history_frame.grid_rowconfigure(1, weight=1)

back_btn = tk.Button(
    history_frame,
    text="« Back »",
    font="Arial 12",
    command=hide_history_frame,
    bg="#1e1e1e",
    fg="#d7ce20",
    highlightbackground="white",
    highlightthickness=5,
    bd=6)
back_btn.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))

history_text = tk.Text(history_frame, font="Arial 12", state=tk.DISABLED,
                       bg="#2e2e2e", fg="white")
history_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

clear_btn = tk.Button(
    history_frame,
    text="Clear History",
    fg="red",
    font="Arial 12 bold",
    bg="#BDE999",
    command=clear_history,
    activebackground="#BDE999",
    width=20)
clear_btn.grid(row=2, column=0, columnspan=2,  pady=(0, 5))

#footer label
footer_label = tk.Label(
    history_frame,
    text="мค∂є вy คкคsн【ツ】",
    font="Arial 11",
    bg="#1e1e1e",
    fg="gray",)
footer_label.grid(row=3,column=0,columnspan=2,pady=(0,10))
# ================================
# Start app
# ================================
load_history()
draw_buttons()

def on_closing():
    save_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
