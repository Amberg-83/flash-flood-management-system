import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import dashboard
import theme


def login_window(root):

    win = ctk.CTkToplevel(root)
    win.title("System Login")
    win.geometry("420x420")
    win.resizable(False, False)

    # bring to front
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(200, lambda: win.attributes("-topmost", False))

    # ================= HEADER =================

    ctk.CTkLabel(
        win,
        text="🔐 OFFICIAL LOGIN",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=25)

    frame = ctk.CTkFrame(win, corner_radius=15)
    frame.pack(padx=30, pady=20, fill="both", expand=True)

    # ================= INPUTS =================

    ctk.CTkLabel(frame, text="Username").pack(anchor="w", padx=25, pady=(20, 5))
    username_entry = ctk.CTkEntry(frame, width=300)
    username_entry.pack(padx=25)

    ctk.CTkLabel(frame, text="Password").pack(anchor="w", padx=25, pady=(15, 5))
    password_entry = ctk.CTkEntry(frame, width=300, show="*")
    password_entry.pack(padx=25)

    # ================= ENSURE ADMIN EXISTS =================

    def ensure_admin():
        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE role='admin'")
        admin = cur.fetchone()

        if not admin:
            cur.execute(
                "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin123", "admin")
            )
            conn.commit()

        conn.close()

    ensure_admin()

    # ================= LOGIN LOGIC =================

    def login():

        u = username_entry.get().strip()
        p = password_entry.get().strip()

        if not u or not p:
            messagebox.showwarning("Input Error", "Please enter username and password")
            return

        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT username, role FROM users WHERE username=? AND password=?",
            (u, p)
        )
        user = cur.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        # ✅ SET SESSION DATA
        root.current_user = user[0]
        root.current_role = user[1]

        win.destroy()
        dashboard.open_dashboard(root)

    # ================= BUTTON =================

    ctk.CTkButton(
        frame,
        text="LOGIN",
        command=login,
        fg_color="#22c55e",
        hover_color="#15803d",
        height=45,
        font=("Segoe UI", 14, "bold")
    ).pack(pady=30)