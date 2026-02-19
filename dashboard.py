import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import simulation, report, ai_predict
import theme


# =========================================================
# ADD USER WINDOW (ADMIN ONLY)
# =========================================================

def add_user_window(parent, root):

    if not hasattr(root, "current_role") or root.current_role != "admin":
        messagebox.showerror("Access Denied", "Only Admin can add users.")
        return

    win = ctk.CTkToplevel(parent)
    win.title("Add New User")
    win.geometry("420x450")
    win.resizable(False, False)

    # bring to front
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(200, lambda: win.attributes("-topmost", False))

    ctk.CTkLabel(
        win,
        text="➕ ADD NEW USER",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=20)

    frame = ctk.CTkFrame(win, corner_radius=15)
    frame.pack(padx=30, pady=20, fill="both", expand=True)

    def field(label, show=None):
        ctk.CTkLabel(frame, text=label).pack(anchor="w", padx=20, pady=(10, 5))
        e = ctk.CTkEntry(frame, width=280, show=show)
        e.pack(padx=20)
        return e

    username = field("Username")
    password = field("Password", show="*")

    ctk.CTkLabel(frame, text="Role").pack(anchor="w", padx=20, pady=(15, 5))
    role = ctk.StringVar(value="officer")

    ctk.CTkOptionMenu(
        frame,
        values=["admin", "officer"],
        variable=role
    ).pack(padx=20)

    def create_user():
        u = username.get().strip()
        p = password.get().strip()
        r = role.get()

        if not u or not p:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
                (u, p, r)
            )
            conn.commit()
            messagebox.showinfo("Success", "User added successfully")
            win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    ctk.CTkButton(
        frame,
        text="CREATE USER",
        fg_color="#22c55e",
        hover_color="#15803d",
        height=45,
        command=create_user
    ).pack(pady=25)


# =========================================================
# MAIN DASHBOARD
# =========================================================

def open_dashboard(root):

    dash = ctk.CTkToplevel(root)
    dash.title("Flood Command Dashboard")
    dash.geometry("950x900")
    dash.resizable(False, False)

    # bring to front
    dash.lift()
    dash.focus_force()
    dash.attributes("-topmost", True)
    dash.after(200, lambda: dash.attributes("-topmost", False))

    # ================= HEADER =================

    ctk.CTkLabel(
        dash,
        text="🌊 INDIA FLASH FLOOD COMMAND CENTER",
        font=("Segoe UI", 24, "bold")
    ).pack(pady=20)

    # ================= USER BAR =================

    user_bar = ctk.CTkFrame(dash, corner_radius=10)
    user_bar.pack(fill="x", padx=30, pady=5)

    ctk.CTkLabel(
        user_bar,
        text=f"👤 User: {getattr(root, 'current_user', 'Unknown')}",
        font=("Segoe UI", 12)
    ).pack(side="left", padx=15, pady=8)

    ctk.CTkLabel(
        user_bar,
        text=f"🔐 Role: {getattr(root, 'current_role', 'N/A').upper()}",
        font=("Segoe UI", 12, "bold"),
        text_color="#38bdf8"
    ).pack(side="right", padx=15)

    # ================= COUNTERS =================

    counter_frame = ctk.CTkFrame(dash)
    counter_frame.pack(pady=15)

    pending_lbl = ctk.CTkLabel(counter_frame, font=("Segoe UI", 14, "bold"))
    critical_lbl = ctk.CTkLabel(counter_frame, font=("Segoe UI", 14, "bold"), text_color="#dc2626")
    resolved_lbl = ctk.CTkLabel(counter_frame, font=("Segoe UI", 14, "bold"), text_color="#22c55e")

    pending_lbl.grid(row=0, column=0, padx=20)
    critical_lbl.grid(row=0, column=1, padx=20)
    resolved_lbl.grid(row=0, column=2, padx=20)

    def update_counters():
        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM civilian_reports WHERE status='Pending'")
        pending = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM civilian_reports
            WHERE severity='Critical' AND status='Pending'
        """)
        critical = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM civilian_reports WHERE status='Resolved'")
        resolved = cur.fetchone()[0]

        conn.close()

        pending_lbl.configure(text=f"🟡 Pending: {pending}")
        critical_lbl.configure(text=f"🔴 Critical: {critical}")
        resolved_lbl.configure(text=f"🟢 Resolved: {resolved}")

        dash.after(2000, update_counters)

    update_counters()

    # ================= CIVILIAN REPORTS =================

    def view_civilian_reports():

        if root.current_role != "admin":
            messagebox.showerror("Access Denied", "Admin access required")
            return

        win = ctk.CTkToplevel(dash)
        win.title("Civilian Reports")
        win.geometry("900x600")

        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        win.after(200, lambda: win.attributes("-topmost", False))

        ctk.CTkLabel(
            win,
            text="📂 CIVILIAN REPORTS (SELECT & RESOLVE)",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        list_frame = ctk.CTkFrame(win)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 12),
            bg="#020617",
            fg="white",
            selectbackground="#2563eb",
            activestyle="none",
            height=18
        )
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        report_ids = []

        def load_reports():
            listbox.delete(0, tk.END)
            report_ids.clear()

            conn = sqlite3.connect("flood_system.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT id, location, severity, status, date
                FROM civilian_reports
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
            conn.close()

            for rid, location, severity, status, date in rows:
                icon = "🔴" if severity == "Critical" else "🟡"
                date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%d %b")
                listbox.insert(
                    tk.END,
                    f"[{date_str}] {icon} {severity} – {location} ({status})"
                )
                report_ids.append(rid)

        load_reports()

        def resolve_selected_report():

            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select a report to resolve.")
                return

            index = sel[0]
            report_id = report_ids[index]

            if not messagebox.askyesno(
                "Confirm Resolution",
                "Resolve selected report?"
            ):
                return

            conn = sqlite3.connect("flood_system.db")
            cur = conn.cursor()
            cur.execute(
                "UPDATE civilian_reports SET status='Resolved' WHERE id=?",
                (report_id,)
            )
            conn.commit()
            conn.close()

            with open("status.txt", "w") as f:
                f.write("normal")

            messagebox.showinfo("Resolved", "Report resolved successfully")
            load_reports()

        ctk.CTkButton(
            win,
            text="✅ RESOLVE SELECTED REPORT",
            fg_color="#22c55e",
            hover_color="#15803d",
            height=45,
            command=resolve_selected_report
        ).pack(pady=15)

    # ================= BUTTONS =================

    ctk.CTkButton(
        dash,
        text="📂 View Civilian Reports",
        fg_color="#f97316",
        height=45,
        command=view_civilian_reports
    ).pack(pady=10)

    if root.current_role == "admin":
        ctk.CTkButton(
            dash,
            text="➕ Add New User",
            fg_color="#0ea5e9",
            hover_color="#0284c7",
            height=45,
            command=lambda: add_user_window(dash, root)
        ).pack(pady=10)

    ctk.CTkButton(
        dash,
        text="🧪 Flood Simulation",
        command=simulation.simulation_window
    ).pack(pady=6)

    ctk.CTkButton(
        dash,
        text="📊 Flood Reports",
        command=report.report_window
    ).pack(pady=6)

    ctk.CTkButton(
        dash,
        text="🧠 AI Prediction",
        fg_color="#22c55e",
        command=ai_predict.ai_window
    ).pack(pady=6)

    ctk.CTkButton(
        dash,
        text="❌ Logout",
        fg_color="#dc2626",
        command=dash.destroy
    ).pack(pady=25)