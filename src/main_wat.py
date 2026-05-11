import customtkinter as ctk
import webbrowser
from PIL import Image
import requests
from io import BytesIO
import project_delta
import threading 

class WatFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, fg_color="#000000", **kwargs)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.foto_label = ctk.CTkLabel(self.scroll, text="", height=240, corner_radius=20)
        self.foto_label.pack_forget()

        self.baslik = ctk.CTkLabel(self.scroll, text="🎒 Work & Travel Rehberi", font=("Segoe UI", 34, "bold"), text_color="#ffffff")
        self.baslik.pack(anchor="w", padx=15)
        self.alt_baslik = ctk.CTkLabel(self.scroll, text="Amerika'yı keşfetmeye hazır mısın? 🇺🇸✨", font=("Segoe UI", 17), text_color="#8e8e93")
        self.alt_baslik.pack(anchor="w", padx=15, pady=(0, 25))

        self.icerik = ctk.CTkFrame(self.scroll, fg_color="#000000")
        self.icerik.pack(fill="both", expand=True)

    def kart_olustur(self, baslik, metin):
        kart = ctk.CTkFrame(self.icerik, fg_color="#1c1c1e", corner_radius=18)
        kart.pack(fill="x", pady=12, padx=12, ipady=15)
        ctk.CTkLabel(kart, text=baslik, font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(anchor="w", padx=25, pady=(18, 8))
        ctk.CTkLabel(kart, text=metin, font=("Segoe UI", 16), text_color="#d1d1d6", wraplength=850, justify="left").pack(anchor="w", padx=25, pady=(0, 18))

    def ekrani_hazirla(self):
        sehir = self.master.son_aranan_sehir
        self.baslik.configure(text=f"🎒 {sehir.upper().split(',')[0]} ÖĞRENCİ REHBERİ")
        self.foto_label.pack_forget()
        for w in self.icerik.winfo_children(): w.destroy()
        
        # Kullanıcıya beklediğini gösteren animasyonlu yazı
        ctk.CTkLabel(self.icerik, text="Yapay Zeka Rehberi Hazırlıyor... ⏳", font=("Segoe UI", 20), text_color="#0a84ff").pack(pady=50)
        
        threading.Thread(target=self.arka_planda_veri_cek, args=(sehir,), daemon=True).start()

    def arka_planda_veri_cek(self, sehir):
        url = project_delta.foto_url_getir(sehir)
        r = project_delta.wat_rehberi_getir(sehir)
        # Veriler hazır olunca arayüzü güncelle
        self.after(0, lambda: self.arayuzu_guncelle(sehir, url, r))

    def arayuzu_guncelle(self, sehir, url, r):
        for w in self.icerik.winfo_children(): w.destroy()
        
        if url:
            try:
                img = Image.open(BytesIO(requests.get(url, timeout=5).content))
                self.foto_label.configure(image=ctk.CTkImage(img, size=(1100, 240)))
                self.foto_label.pack(fill="x", pady=(0, 20), before=self.baslik)
            except: pass

        if r.get("mekanlar"):
            btn_frame = ctk.CTkFrame(self.icerik, fg_color="#000000")
            btn_frame.pack(fill="x", padx=15, pady=(0, 15))
            ctk.CTkLabel(btn_frame, text="📍 Haritada Görmek İçin Tıklayın:", font=("Segoe UI", 16, "bold")).pack(side="left", padx=(0, 20))
            for m in r["mekanlar"]:
                ctk.CTkButton(btn_frame, text=f"🗺️ {m}", fg_color="#0a84ff", corner_radius=22, font=("Segoe UI", 14, "bold"), command=lambda x=m: webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={x}+{sehir}")).pack(side="left", padx=5)

        self.kart_olustur("🍔 Nerede Ne Yenir?", r.get("yemek", "Bulunamadı."))
        self.kart_olustur("💸 Ortalama Günlük Masraf", r.get("butce", "Bulunamadı."))
        self.kart_olustur("🎒 J1 Öğrencisi İçin İpucu", r.get("ipucu", "Bulunamadı."))
