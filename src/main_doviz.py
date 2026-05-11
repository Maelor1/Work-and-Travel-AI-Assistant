import customtkinter as ctk
import project_delta

class DovizFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, fg_color="#000000", **kwargs)
        self.kutu = ctk.CTkFrame(self, corner_radius=18, width=450, fg_color="#1c1c1e")
        self.kutu.pack(pady=100)
        ctk.CTkLabel(self.kutu, text="💵 Döviz Çevirici", font=("Segoe UI", 26, "bold")).pack(pady=30, padx=60)
        self.inp = ctk.CTkEntry(self.kutu, placeholder_text="Miktar...", width=250); self.inp.pack(pady=10)
        self.yon = ctk.StringVar(value="USD_TO_TRY")
        ctk.CTkRadioButton(self.kutu, text="USD -> TRY", variable=self.yon, value="USD_TO_TRY").pack()
        ctk.CTkRadioButton(self.kutu, text="TRY -> USD", variable=self.yon, value="TRY_TO_USD").pack()
        ctk.CTkButton(self.kutu, text="Hesapla", command=self.calc).pack(pady=20)
        self.res = ctk.CTkLabel(self.kutu, text="Sonuç: --", font=("Segoe UI", 24, "bold"), text_color="#ffd60a"); self.res.pack(pady=20)

    def calc(self):
        kur = project_delta.dolar_kuru_cek()
        if kur != "Hata": self.res.configure(text=project_delta.para_cevir(self.inp.get(), kur, self.yon.get()))