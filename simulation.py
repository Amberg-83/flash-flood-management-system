import customtkinter as ctk
import random
import sqlite3
import datetime
import theme   # apply global theme


def simulation_window():

    win = ctk.CTkToplevel()
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(200, lambda: win.attributes("-topmost", False))
    win.title("Flood Scenario Simulation")
    win.geometry("520x620")
    win.resizable(False, False)

    # ================= HEADER =================

    ctk.CTkLabel(
        win,
        text="🌊 FLASH FLOOD SIMULATION PANEL",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        win,
        text="Generate synthetic flood scenarios for analysis",
        font=("Segoe UI", 12),
        text_color="#94a3b8"
    ).pack(pady=5)

    # ================= CARD =================

    card = ctk.CTkFrame(win, corner_radius=15)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    # ================= STATE SELECTION =================

    ctk.CTkLabel(
        card,
        text="Select State",
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", padx=20, pady=(20, 5))

    state_var = ctk.StringVar(value="Uttarakhand")

    states = [
        "Uttarakhand",
        "Assam",
        "Kerala",
        "Bihar",
        "Himachal Pradesh"
    ]

    ctk.CTkOptionMenu(
        card,
        values=states,
        variable=state_var,
        width=250
    ).pack(padx=20, pady=10)

    # ================= OUTPUT =================

    output = ctk.CTkTextbox(
        card,
        height=220,
        font=("Consolas", 12)
    )
    output.pack(fill="x", padx=20, pady=20)
    output.insert("end", "Simulation results will appear here...")
    output.configure(state="disabled")

    # ================= SIMULATION LOGIC =================

    def run():

        state = state_var.get()

        rainfall = random.uniform(80, 250)
        river = random.uniform(3, 10)
        pop = random.randint(200, 1200)
        drainage = random.randint(20, 80)
        resources = random.randint(30, 150)

        affected = int(
            rainfall * 5 +
            river * 200 +
            pop * 2 -
            drainage * 10 -
            resources * 8
        )

        if affected < 0:
            affected = random.randint(100, 500)

        date = datetime.date.today()

        conn = sqlite3.connect("flood_system.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO flood_data
            (state, rainfall, river_level,
             population_density, drainage_capacity,
             resources_deployed, affected_population, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            state,
            rainfall,
            river,
            pop,
            drainage,
            resources,
            affected,
            str(date)
        ))

        conn.commit()
        conn.close()

        result = f"""
State: {state}
Rainfall (mm/hr): {rainfall:.2f}
River Level (m): {river:.2f}
Population Density: {pop}
Drainage Capacity: {drainage}
Resources Deployed: {resources}
Affected Population: {affected}
Date: {date}
"""

        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("end", result)
        output.configure(state="disabled")

    # ================= ACTION BUTTON =================

    ctk.CTkButton(
        win,
        text="▶ RUN FLOOD SIMULATION",
        command=run,
        fg_color="#22c55e",
        hover_color="#15803d",
        height=45,
        width=280,
        font=("Segoe UI", 14, "bold")
    ).pack(pady=15)