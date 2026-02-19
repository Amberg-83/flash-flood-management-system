import customtkinter as ctk
import pickle
import sqlite3
from tkinter import messagebox
from datetime import date
import sklearn

def ai_window():
    win = ctk.CTkToplevel()
    win.title("AI Flood Prediction Console")
    
    width = 800
    height = 900
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.resizable(True, True)
    
    win.lift()
    win.attributes("-topmost", True)
    win.after(100, lambda: win.attributes("-topmost", False))
    win.grab_set()
    win.focus_force()

    ctk.CTkLabel(
        win,
        text="🌊 AI FLASH FLOOD ANALYSIS PANEL",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        win,
        text="Random Forest–based Flood Impact Prediction",
        font=("Segoe UI", 12),
        text_color="#94a3b8"
    ).pack(pady=(0, 10))

    card = ctk.CTkScrollableFrame(win, corner_radius=15)
    card.pack(padx=40, pady=10, fill="both", expand=True)

    ctk.CTkLabel(
        card,
        text="Select State",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", padx=30, pady=(20, 5))

    states = [
        "Uttarakhand", "Assam", "Kerala", "Bihar", "Himachal Pradesh",
        "West Bengal", "Odisha", "Tamil Nadu", "Maharashtra",
        "Gujarat", "Rajasthan"
    ]

    state_var = ctk.StringVar(value="Uttarakhand")

    ctk.CTkOptionMenu(
        card,
        values=states,
        variable=state_var,
        width=300
    ).pack(padx=30, pady=10)

    fields = {}

    def slider(label, frm, to):
        ctk.CTkLabel(
            card,
            text=label,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=30, pady=(15, 5))

        value_lbl = ctk.CTkLabel(
            card,
            text=str(frm),
            font=("Segoe UI", 11),
            text_color="#94a3b8"
        )
        value_lbl.pack(anchor="e", padx=40)

        s = ctk.CTkSlider(
            card,
            from_=frm,
            to=to,
            number_of_steps=to - frm,
            width=520
        )
        s.pack(padx=30, pady=6)
        s.configure(command=lambda v, lbl=value_lbl: lbl.configure(text=str(int(v))))
        fields[label] = s

    slider("Rainfall (mm/hr)", 0, 300)
    slider("River Level (m)", 0, 12)
    slider("Population Density", 100, 1500)
    slider("Drainage Capacity", 10, 100)
    slider("Resources Deployed", 10, 200)

    result_lbl = ctk.CTkLabel(
        card,
        text="Predicted Affected Population: --",
        font=("Segoe UI", 16, "bold")
    )
    result_lbl.pack(pady=(30, 5))

    confidence_lbl = ctk.CTkLabel(
        card,
        text="Confidence: --",
        font=("Segoe UI", 13, "bold"),
        text_color="#38bdf8"
    )
    confidence_lbl.pack(pady=5)

    status_lbl = ctk.CTkLabel(
        card,
        text="Status: Waiting...",
        font=("Segoe UI", 14, "bold")
    )
    status_lbl.pack(pady=10)

    def predict():
        try:
            with open("flood_model.pkl", "rb") as model_file:
                model = pickle.load(model_file)

            state_code = states.index(state_var.get())
            values = [
                state_code,
                fields["Rainfall (mm/hr)"].get(),
                fields["River Level (m)"].get(),
                fields["Population Density"].get(),
                fields["Drainage Capacity"].get(),
                fields["Resources Deployed"].get()
            ]

            pred = int(model.predict([values])[0])
            tree_preds = [int(tree.predict([values])[0]) for tree in model.estimators_]
            spread = max(tree_preds) - min(tree_preds)
            confidence = max(50, 100 - (spread / max(pred, 1)) * 100)

            result_lbl.configure(text=f"Predicted Affected Population: {pred}")
            confidence_lbl.configure(text=f"Confidence: {confidence:.1f}%")

            if pred < 1000:
                level, msg, color = "normal", "SAFE", "#22c55e"
            elif pred < 3000:
                level, msg, color = "moderate", "FLOOD WARNING", "#facc15"
            elif pred < 6000:
                level, msg, color = "high", "FLOOD EMERGENCY", "#fb7185"
            else:
                level, msg, color = "severe", "SEVERE FLASH FLOOD", "#dc2626"

            status_lbl.configure(text=f"Status: {msg}", text_color=color)

            with open("status.txt", "w") as f:
                f.write(level)

            conn = sqlite3.connect("flood_system.db")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ai_predictions 
                (state, rainfall, river_level, pop_density, drainage, 
                 resources, predicted_affected, confidence, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                state_var.get(),
                fields["Rainfall (mm/hr)"].get(),
                fields["River Level (m)"].get(),
                fields["Population Density"].get(),
                fields["Drainage Capacity"].get(),
                fields["Resources Deployed"].get(),
                pred,
                round(confidence, 2),
                str(date.today())
            ))
            conn.commit()
            conn.close()

        except FileNotFoundError:
            messagebox.showerror("Error", "flood_model.pkl not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(
        card,
        text="🧠 RUN AI ANALYSIS",
        command=predict,
        fg_color="#22c55e",
        hover_color="#15803d",
        width=360,
        height=50,
        font=("Segoe UI", 15, "bold")
    ).pack(pady=(25, 20))

    ctk.CTkButton(
        card,
        text="Close Window",
        command=win.destroy,
        fg_color="transparent",
        border_width=1,
        text_color="#94a3b8",
        width=150
    ).pack(pady=(0, 40))

if __name__ == "__main__":
    root = ctk.CTk()
    btn = ctk.CTkButton(root, text="Open AI Panel", command=ai_window)
    btn.pack(pady=20)
    root.mainloop()