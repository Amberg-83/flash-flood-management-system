import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import date
import theme


def civilian_portal():

    win = ctk.CTk()
    win.title("Civilian Flood Report Portal")
    win.geometry("520x650")

    ctk.CTkLabel(
        win,
        text="🚨 REPORT FLOOD INCIDENT",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=25)

    name = ctk.CTkEntry(win, placeholder_text="Your Name")
    name.pack(padx=40, pady=10, fill="x")

    location = ctk.CTkEntry(win, placeholder_text="Location")
    location.pack(padx=40, pady=10, fill="x")

    desc = ctk.CTkTextbox(win, height=120)
    desc.pack(padx=40, pady=10, fill="x")
    desc.insert("end", "Describe the situation...")

    severity = ctk.StringVar(value="High")
    ctk.CTkOptionMenu(
        win,
        values=["Low", "High", "Critical"],
        variable=severity
    ).pack(pady=15)

    def submit():
        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO civilian_reports
            (name, location, description, severity, status, date)
            VALUES (?,?,?,?,?,?)
        """, (
            name.get(),
            location.get(),
            desc.get("1.0", "end"),
            severity.get(),
            "Pending",
            str(date.today())
        ))

        conn.commit()
        conn.close()

        if severity.get() == "Critical":
            with open("status.txt", "w") as f:
                f.write("severe")

        messagebox.showinfo("Submitted", "Report sent successfully")
        win.destroy()

    ctk.CTkButton(
        win,
        text="SUBMIT REPORT",
        fg_color="#dc2626",
        height=45,
        command=submit
    ).pack(pady=25)

    win.mainloop()