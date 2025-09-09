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
        self.root.title("Password Manager GUI")
        self.root.configure(bg="#2f2f2f")

        # Labels
        self.label1 = tk.Label(
            root,
            text="Generating Random Password",
            font=('Arial', 18),
            bg="#2f2f2f",
            fg="white"
        )
        self.label1.pack(pady=20)

        self.label2 = tk.Label(
            root,
            text="Password must be at least 8 characters long and contain:\n"
                 "- • At least one letter\n"
                 "- • At least one number\n"
                 "- • At least one special character!",
            font=('Arial', 18),
            bg="#2f2f2f",
            fg="white"
        )
        self.label2.pack(pady=20)

        # Frame with grid layout
        self.frame = tk.Frame(
            root,
            borderwidth=6,
            bg="grey",
            relief=tk.SUNKEN,
            width=700,
            height=150
        )
        self.frame.pack(pady=40)
        self.frame.pack_propagate(False)

        # Row 0: Entry + Buttons (all inline)
        self.myentry = tk.Entry(self.frame, width=30, state="readonly")
        self.myentry.grid(row=0, column=0, padx=10, pady=20)

        img = Image.open("pencil-fill.png")
        img = img.resize((15, 15), Image.Resampling.LANCZOS)
        self.edit = ImageTk.PhotoImage(img)
        self.b1 = tk.Button(
            self.frame, image=self.edit, width=30, height=30,
            bg="lightblue", command=self.enable_edit
        )
        self.b1.grid(row=0, column=1, padx=10, pady=20)

        img2 = Image.open("clipboard.png")
        img2 = img2.resize((15, 15), Image.Resampling.LANCZOS)
        self.clipboard_img = ImageTk.PhotoImage(img2)
        self.b3 = tk.Button(
            self.frame, image=self.clipboard_img, width=30, height=30,
            bg="lightblue", command=self.copy_to_clipboard
        )
        self.b3.grid(row=0, column=2, padx=10, pady=20)

        self.b2 = tk.Button(
            self.frame, bg="lightblue", fg="black",
            text="Generate Password", width=18, height=1,
            command=self.on_click
        )
        self.b2.grid(row=0, column=3, padx=10, pady=20)

        self.check_btn = tk.Button(
            self.frame, text="Check Password",
            bg="lightblue", fg="black",
            width=18, height=1,
            command=self.validate_password
        )
        self.check_btn.grid(row=0, column=4, padx=10, pady=20)

        # Row 1: Slider only
        self.slider_value = tk.IntVar(value=12)
        style = ttk.Style()
        style.configure("TScale", troughcolor="lightgrey", background="blue")
        

        self.slider = ttk.Scale(
            self.frame, from_=8, to=32,
            orient="horizontal", length=600,variable=self.slider_value,
    command=lambda e: self.update_length_label()
        )
        self.slider.set(12)  # default value
        self.slider.grid(row=1, column=0, columnspan=5, pady=10)
        

        self.length_label = tk.Label(
        self.frame,
        text=f"Length = {self.slider_value.get()}",
        font=('Arial', 14),
        bg="grey",
        fg="white"
        )
        self.length_label.grid(row=2, column=0, columnspan=5, pady=5)

    def update_length_label(self):
        self.length_label.config(text=f"Length = {self.slider_value.get()}")


    # Enable editing of entry
    def enable_edit(self):
        if self.myentry.cget("state") == "readonly":
            self.myentry.config(state="normal")
            self.myentry.focus_set()
        else:
            self.myentry.config(state="readonly")

    # Generate random password
    def generate_password(self, length=None):
        if length is None:
            length = self.slider_value.get()  # get the current slider value
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))


    # Insert generated password into entry
    def on_click(self):
        self.myentry.config(state="normal")
        length = int(self.slider.get())  # take length from slider
        password = self.generate_password(length)
        self.myentry.delete(0, tk.END)
        self.myentry.insert(0, password)
        self.myentry.config(state="readonly")

    # Copy entry content to clipboard
    def copy_to_clipboard(self):
        text = self.myentry.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    # Validate password
    def validate_password(self):
        text = self.myentry.get()
        required_value = self.slider_value.get()
        has_letter = re.search(r"[A-Za-z]", text)
        has_digit = re.search(r"\d", text)
        has_special = re.search(r"[^A-Za-z0-9]", text)

        if len(text) < required_value or not has_letter or not has_digit or not has_special:
            messagebox.showerror(
                "Invalid Password",
                "Password must be at least 8 characters long and contain:\n"
                "- At least one letter\n"
                "- At least one number\n"
                "- At least one special character!"
            )
        else:
            messagebox.showinfo("Valid Password", "Password is valid!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
