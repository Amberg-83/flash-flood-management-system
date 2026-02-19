import customtkinter as ctk
import login
import civilian
import theme   # applies global theme


def main():

    root = ctk.CTk()
    root.lift()
    root.focus_force()
    root.title("India Flash Flood Management System")
    root.geometry("650x520")
    root.resizable(False, False)

    # ================= HEADER =================

    ctk.CTkLabel(
        root,
        text="🌊 INDIA FLASH FLOOD\nMANAGEMENT SYSTEM",
        font=("Segoe UI", 26, "bold"),
        justify="center"
    ).pack(pady=35)

    ctk.CTkLabel(
        root,
        text="Disaster Reporting & Command Center",
        font=("Segoe UI", 14),
        text_color="#94a3b8"
    ).pack(pady=5)

    # ================= BUTTON CARD =================

    card = ctk.CTkFrame(root, corner_radius=15)
    card.pack(pady=40, padx=40, fill="both", expand=True)

    # ================= BUTTONS =================

    ctk.CTkButton(
        card,
        text="🔐 Official Login",
        width=320,
        height=50,
        font=("Segoe UI", 15, "bold"),
        command=lambda: login.login_window(root)
    ).pack(pady=18)

    ctk.CTkButton(
        card,
        text="🚨 Civilian Report Portal",
        width=320,
        height=50,
        font=("Segoe UI", 15, "bold"),
        fg_color="#dc2626",
        hover_color="#991b1b",
        command=civilian.civilian_portal
    ).pack(pady=18)

    ctk.CTkButton(
        card,
        text="❌ Exit",
        width=320,
        height=45,
        font=("Segoe UI", 14, "bold"),
        fg_color="#374151",
        hover_color="#111827",
        command=root.destroy
    ).pack(pady=25)

    root.mainloop()


if __name__ == "__main__":
    main()