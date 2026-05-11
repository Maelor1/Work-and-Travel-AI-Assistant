import customtkinter as ctk
import project_delta
import threading # 🌟 YENİ EKLENDİ
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    import pytz as ZoneInfo

class AnaEkranFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, fg_color="#000000", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        # --- 🕒 AMERİKA EYALET SAATİ ---
        self.saat_karti = ctk.CTkFrame(self, fg_color="#1c1c1e", corner_radius=20)
        self.saat_karti.pack(pady=(40, 20), padx=50, fill="x")

        self.eyaletler = {
            "New Jersey (Icona Avalon)": "America/New_York",
            "New York (NYC)": "America/New_York",
            "Florida (Miami)": "America/New_York",
            "Illinois (Chicago)": "America/Chicago",
            "Texas (Austin)": "America/Chicago",
            "Colorado (Denver)": "America/Denver",
            "California (LA)": "America/Los_Angeles",
            "Washington (Seattle)": "America/Los_Angeles"
        }

        ctk.CTkLabel(self.saat_karti, text="🇺🇸 AMERİKA YEREL SAAT", font=("Segoe UI", 16, "bold"), text_color="#8e8e93").pack(pady=(15, 5))
        self.eyalet_secici = ctk.CTkOptionMenu(self.saat_karti, values=list(self.eyaletler.keys()), command=self.saat_guncelle, fg_color="#2c2c2e", button_color="#3a3a3c", width=250, corner_radius=12)
        self.eyalet_secici.set("New Jersey (Icona Avalon)")
        self.eyalet_secici.pack(pady=10)
        self.eyalet_saati_label = ctk.CTkLabel(self.saat_karti, text="--:--", font=("Segoe UI", 56, "bold"), text_color="#ffd60a")
        self.eyalet_saati_label.pack(pady=(5, 15))

        # --- ✈️ GERİ SAYIM ---
        ctk.CTkLabel(self, text="YOLCULUĞA KALAN SÜRE", font=("Segoe UI", 20, "bold"), text_color="#8e8e93").pack(pady=(40, 10))
        self.zaman = ctk.CTkLabel(self, text="Hesaplanıyor...", font=("Segoe UI", 42, "bold"), text_color="#0a84ff")
        self.zaman.pack(pady=10)

        # --- 💵 DOLAR KURU ---
        self.kur_karti = ctk.CTkFrame(self, fg_color="#1c1c1e", corner_radius=20)
        self.kur_karti.pack(pady=30, padx=100, fill="x")
        ctk.CTkLabel(self.kur_karti, text="GÜNCEL DOLAR KURU", font=("Segoe UI", 16, "bold"), text_color="#8e8e93").pack(pady=(15, 0))
        self.kur = ctk.CTkLabel(self.kur_karti, text="Yükleniyor... ⏳", font=("Segoe UI", 32, "bold"), text_color="#30d158")
        self.kur.pack(pady=(5, 15))

        self.donguyu_baslat()

    def saat_guncelle(self, secilen_eyalet=None):
        if not secilen_eyalet: secilen_eyalet = self.eyalet_secici.get()
        timezone_id = self.eyaletler.get(secilen_eyalet, "America/New_York")
        try:
            yerel_saat = datetime.now(ZoneInfo(timezone_id)).strftime("%H:%M")
            self.eyalet_saati_label.configure(text=yerel_saat)
        except Exception as e:
            self.eyalet_saati_label.configure(text="Hata")

    # 🌟 OPTİMİZASYON: Dolar kurunu arayüzü dondurmadan arka planda çeker
    def dolar_kuru_getir_arka_plan(self):
        kur_degeri = project_delta.dolar_kuru_cek()
        # Veri gelince arayüzü günceller (.after komutu arayüzün çökmesini engeller)
        self.after(0, lambda: self.kur.configure(text=f"{kur_degeri} ₺"))

    def donguyu_baslat(self):
        self.saat_guncelle()
        self.zaman.configure(text=project_delta.kalan_zamani_hesapla("2026-06-13 10:00:00"))
        
        # Dolar kurunu dondurmadan ayrı bir işçi (thread) ile başlat
        threading.Thread(target=self.dolar_kuru_getir_arka_plan, daemon=True).start()
        
        self.after(60000, self.donguyu_baslat)