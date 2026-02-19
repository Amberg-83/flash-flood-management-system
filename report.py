import customtkinter as ctk
import sqlite3
from datetime import datetime
# import theme  # Ensure theme.py exists in your directory

def report_window():
    win = ctk.CTkToplevel()
    win.title("Flood Incident Reports")
    win.geometry("900x600")
    win.resizable(False, False)

    # ================= BRING TO FRONT =================
    win.lift()                          # Lift window above others
    win.attributes('-topmost', True)    # Temporarily force to top
    win.after(10, lambda: win.attributes('-topmost', False)) # Allow other windows to overlap later
    win.grab_set()                      # Prevent interaction with main window until closed
    win.focus_force()                   # Force keyboard focus

    # ================= HEADER =================

    ctk.CTkLabel(
        win,
        text="🌊 FLOOD INCIDENT REPORTS",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        win,
        text="Historical & Predicted Flood Data",
        font=("Segoe UI", 13),
        text_color="#94a3b8"
    ).pack(pady=(0, 10))

    # ================= TABLE FRAME =================

    frame = ctk.CTkFrame(win, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Using a scrollable text box to view the data
    textbox = ctk.CTkTextbox(
        frame,
        font=("Consolas", 12),
        wrap="none"
    )
    textbox.pack(fill="both", expand=True, padx=15, pady=15)

    # ================= LOAD DATA =================

    try:
        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()
        
        # Check if table exists before querying
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flood_data'")
        if cur.fetchone():
            cur.execute("SELECT * FROM flood_data")
            data = cur.fetchall()
        else:
            data = []
            
        conn.close()

        # Table Header Formatting
        header = f"{'ID':<4} | {'State':<15} | {'Rain':<6} | {'RivL':<6} | {'PopD':<6} | {'Drain':<6} | {'Res':<6} | {'Affct':<6} | {'Date'}\n"
        textbox.insert("end", header)
        textbox.insert("end", "=" * 100 + "\n")

        if not data:
            textbox.insert("end", "\n[ NO RECORDS FOUND IN DATABASE ]")
        else:
            for row in data:
                # Format row values to align with headers
                formatted_row = " | ".join(f"{str(item):<6}" if i > 1 else f"{str(item):<15}" for i, item in enumerate(row))
                textbox.insert("end", f"{formatted_row}\n")

    except Exception as e:
        textbox.insert("end", f"Error loading database: {str(e)}")

    textbox.configure(state="disabled") # Make read-only

    # ================= CLOSE BUTTON =================
    ctk.CTkButton(
        win, 
        text="Close Reports", 
        command=win.destroy,
        fg_color="#3b82f6",
        hover_color="#2563eb"
    ).pack(pady=(0, 20))

# To test standalone:
if __name__ == "__main__":
    root = ctk.CTk()
    btn = ctk.CTkButton(root, text="Open Reports", command=report_window)
    btn.pack(pady=40)
    root.mainloop()