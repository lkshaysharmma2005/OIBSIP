import tkinter as tk
from PIL import Image, ImageTk
import random
import string
import re
from tkinter import messagebox, ttk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Password Manager")
        self.root.configure(bg="#2f2f2f")

        self.label1 = tk.Label(root, text="🔐 Password Manager", font=('Arial', 22, "bold"), bg="#2f2f2f", fg="white")
        self.label1.pack(pady=10)

        self.label2 = tk.Label(root,
            text="Password must be at least 8 characters and include:\n• A letter\n• A number\n• A special character",
            font=('Arial', 14), bg="#2f2f2f", fg="lightgrey", justify="left")
        self.label2.pack(pady=10)

        self.frame = tk.Frame(root, bg="#404040", bd=2, relief=tk.RIDGE, width=800, height=300)
        self.frame.pack(pady=30)
        self.frame.pack_propagate(False)

        button_frame = tk.Frame(self.frame, bg="#404040")
        button_frame.pack(pady=15)

        self.easy = tk.Button(button_frame, text="Easy", bg="#09829D", fg="white", font=("Arial", 12, "bold"),
                              width=10, command=lambda: self.generate_password("easy"))
        self.easy.grid(row=0, column=0, padx=10)

        self.medium = tk.Button(button_frame, text="Medium", bg="#09829D", fg="white", font=("Arial", 12, "bold"),
                                width=10, command=lambda: self.generate_password("medium"))
        self.medium.grid(row=0, column=1, padx=10)

        self.hard = tk.Button(button_frame, text="Hard", bg="#09829D", fg="white", font=("Arial", 12, "bold"),
                              width=10, command=lambda: self.generate_password("hard"))
        self.hard.grid(row=0, column=2, padx=10)

        entry_frame = tk.Frame(self.frame, bg="#404040")
        entry_frame.pack(pady=15)

        self.myentry = tk.Entry(entry_frame, width=20, font=("Arial", 14), state="readonly", justify="center")
        self.myentry.grid(row=0, column=0, padx=10)

        img = Image.open("pencil-fill.png").resize((18, 18), Image.Resampling.LANCZOS)
        self.edit = ImageTk.PhotoImage(img)
        self.b1 = tk.Button(entry_frame, image=self.edit, bg="#2196F3", command=self.enable_edit)
        self.b1.grid(row=0, column=1, padx=5)

        img2 = Image.open("clipboard.png").resize((18, 18), Image.Resampling.LANCZOS)
        self.clipboard_img = ImageTk.PhotoImage(img2)
        self.b2 = tk.Button(entry_frame, image=self.clipboard_img, bg="#9C27B0", command=self.copy_to_clipboard)
        self.b2.grid(row=0, column=2, padx=5)

        self.b3 = tk.Button(entry_frame, text="Generate Password", bg="#009688", fg="white",
                            font=("Arial", 12, "bold"), width=18, command=self.on_click)
        self.b3.grid(row=0, column=3, padx=10)

        self.check_btn = tk.Button(entry_frame, text="Check Password", bg="#795548", fg="white",
                                   font=("Arial", 12, "bold"), width=18, command=self.validate_password)
        self.check_btn.grid(row=0, column=4, padx=10)

        slider_frame = tk.Frame(self.frame, bg="#404040")
        slider_frame.pack(pady=20)

        self.slider_value = tk.IntVar(value=12)
        style = ttk.Style()
        style.configure("TScale", troughcolor="lightgrey", background="blue")

        self.slider = ttk.Scale(slider_frame, from_=8, to=32, orient="horizontal", length=600,
                                variable=self.slider_value, command=lambda e: self.update_length_label())
        self.slider.grid(row=0, column=0, pady=10)

        self.difficulty = tk.StringVar(value="Custom")

        self.length_label = tk.Label(slider_frame,
            text=f"Length = {self.slider_value.get()} | Difficulty = {self.difficulty.get()}",
            font=('Arial', 14), bg="#404040", fg="white")
        self.length_label.grid(row=1, column=0, pady=5)

    def update_length_label(self):
        self.length_label.config(text=f"Length = {self.slider_value.get()} | Difficulty = {self.difficulty.get()}")

    def enable_edit(self):
        if self.myentry.cget("state") == "readonly":
            self.myentry.config(state="normal")
            self.myentry.focus_set()
        else:
            self.myentry.config(state="readonly")

    def generate_password(self, level):
        length = 8 if level == "easy" else 12 if level == "medium" else 16
        letters, digits, specials = string.ascii_letters, string.digits, string.punctuation
        password = [random.choice(letters), random.choice(digits), random.choice(specials)]
        all_chars = letters + digits + specials
        password += [random.choice(all_chars) for _ in range(length - 3)]
        random.shuffle(password)
        password = ''.join(password)

        self.difficulty.set(level.capitalize())
        self.slider_value.set(length)
        self.update_length_label()
        self.myentry.config(state="normal")
        self.myentry.delete(0, tk.END)
        self.myentry.insert(0, password)
        self.myentry.config(state="readonly")

    def on_click(self):
        self.myentry.config(state="normal")
        length = int(self.slider.get())
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        self.difficulty.set("Custom")
        self.update_length_label()
        self.myentry.delete(0, tk.END)
        self.myentry.insert(0, password)
        self.myentry.config(state="readonly")

    def copy_to_clipboard(self):
        text = self.myentry.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Password copied!")

    def validate_password(self):
        text = self.myentry.get()
        required_value = self.slider_value.get()
        has_letter, has_digit, has_special = re.search(r"[A-Za-z]", text), re.search(r"\d", text), re.search(r"[^A-Za-z0-9]", text)
        if len(text) < required_value or not has_letter or not has_digit or not has_special:
            messagebox.showerror("Invalid", "Password must have:\n- A letter\n- A number\n- A special character")
        else:
            messagebox.showinfo("Valid", "Password is strong!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
