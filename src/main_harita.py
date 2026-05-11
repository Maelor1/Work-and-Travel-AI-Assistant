import customtkinter as ctk
import tkintermapview
from PIL import Image
import requests
from io import BytesIO
import webbrowser
import project_delta
import threading 

class HaritaFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#000000", **kwargs)
        self._arama_timer = None
        
        self.sol = ctk.CTkScrollableFrame(self, width=430, fg_color="#000000")
        self.sol.pack(side="left", fill="y", padx=10)
        self.ara = ctk.CTkEntry(self.sol, placeholder_text="Şehir ara...", width=390, height=45, corner_radius=22, font=("Segoe UI", 16))
        self.ara.pack(pady=15)
        self.ara.bind("<KeyRelease>", self.on_key_release)
        self.ara.bind("<Return>", lambda e: self.islem())
        
        self.oneri_frame = ctk.CTkFrame(self.sol, fg_color="#000000")
        self.oneri_frame.pack(fill="x")
        self.foto = ctk.CTkLabel(self.sol, text="", height=220, corner_radius=18)
        self.foto.pack_forget()
        self.baslik = ctk.CTkLabel(self.sol, text="Hedef Seç", font=("Segoe UI", 26, "bold"), text_color="#ffffff")
        self.baslik.pack(pady=(5,0), anchor="w", padx=10)
        self.mesafe = ctk.CTkLabel(self.sol, text="", font=("Segoe UI", 14), text_color="#8e8e93")
        self.mesafe.pack(pady=(0,10), anchor="w", padx=10)
        self.biletler = ctk.CTkFrame(self.sol, fg_color="#000000")
        self.biletler.pack(fill="x")
        
        self.icerik_kart = ctk.CTkFrame(self.sol, fg_color="#1c1c1e", corner_radius=18)
        self.icerik_kart.pack(fill="x", pady=15, ipady=15)
        self.rehber_ozet = ctk.CTkLabel(self.icerik_kart, text="Haritadan bir şehir arat...", font=("Segoe UI", 16), wraplength=350, justify="left")
        self.rehber_ozet.pack(padx=20, pady=15)
        self.rehber_yerler = ctk.CTkLabel(self.icerik_kart, text="", font=("Segoe UI", 16, "bold"), text_color="#30d158", justify="left")
        self.rehber_yerler.pack(padx=20, pady=(0, 10), anchor="w")

        self.harita_sag = ctk.CTkFrame(self, corner_radius=18, fg_color="#1c1c1e")
        self.harita_sag.pack(side="right", fill="both", expand=True, padx=20, pady=10)
        
        self.ust_bar = ctk.CTkFrame(self.harita_sag, fg_color="#1c1c1e")
        self.ust_bar.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(self.ust_bar, text="🗺️ Görünüm:", font=("Segoe UI", 15, "bold")).pack(side="left", padx=10)
        self.stil_secici = ctk.CTkOptionMenu(self.ust_bar, values=["Karanlık Mod", "Google Maps", "Google Uydu", "Açık Renk"], command=self.stili_degistir)
        self.stil_secici.pack(side="left")
        
        self.harita = tkintermapview.TkinterMapView(self.harita_sag, corner_radius=15)
        self.harita.pack(fill="both", expand=True, padx=10, pady=10)
        self.stili_degistir("Karanlık Mod")
        self.harita.set_zoom(2)

    def on_key_release(self, event):
        if event.keysym == 'Return': return
        if self._arama_timer: self.after_cancel(self._arama_timer)
        self._arama_timer = self.after(500, self.onerileri_ara)

    def onerileri_ara(self):
        metin = self.ara.get()
        for w in self.oneri_frame.winfo_children(): w.destroy()
        if len(metin) > 2:
            for y in project_delta.onerileri_getir(metin):
                ctk.CTkButton(self.oneri_frame, text=y[:50], anchor="w", width=390, fg_color="#1c1c1e", command=lambda yer=y: self.oneri_sec(yer)).pack(pady=2)

    def oneri_sec(self, secilen_yer):
        self.ara.delete(0, 'end'); self.ara.insert(0, secilen_yer)
        for w in self.oneri_frame.winfo_children(): w.destroy()
        self.islem()

    def stili_degistir(self, secim):
        if secim == "Google Maps": self.harita.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif secim == "Google Uydu": self.harita.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif secim == "Karanlık Mod": self.harita.set_tile_server("https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png", max_zoom=19)
        elif secim == "Açık Renk": self.harita.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=19)

    def islem(self):
        sehir = self.ara.get()
        if not sehir: return
        for w in self.oneri_frame.winfo_children(): w.destroy()
        
        # Arayüzü bekleme moduna al
        self.foto.pack_forget()
        self.mesafe.configure(text="Konum hesaplanıyor... ⏳")
        self.rehber_ozet.configure(text="Yapay zeka analiz ediyor... ⏳")
        self.rehber_yerler.configure(text="")
        for w in self.biletler.winfo_children(): w.destroy()
        ctk.CTkLabel(self.biletler, text="Biletler aranıyor... 🛫", font=("Segoe UI", 14), text_color="#8e8e93").pack(pady=10)
        
        # OPTİMİZASYON: Zorlu işlemleri arka plana at
        threading.Thread(target=self.arka_plan_verileri_topla, args=(sehir,), daemon=True).start()

    def arka_plan_verileri_topla(self, sehir):
        sehir_kisa = sehir.split(",")[0].strip()
        project_delta.aranan_sehre_profil_ekle(sehir_kisa)
        self.master.son_aranan_sehir = sehir
        
        v = project_delta.mesafe_ve_koordinat_bul(sehir)
        r = project_delta.gezilecek_yerleri_bul(sehir)
        url = project_delta.foto_url_getir(sehir)
        blt = []
        if v.get("durum"):
            blt = project_delta.gercek_bilet_bul(v.get("benim_sehir", "Istanbul"), sehir_kisa)

        # Veriler toplanınca arayüzü güncelle
        self.after(0, lambda: self.haritayi_guncelle(v, r, url, blt, sehir_kisa, sehir))

    def haritayi_guncelle(self, v, r, url, blt, sehir_kisa, sehir):
        if v.get("durum"):
            self.harita.delete_all_marker(); self.harita.delete_all_path()
            self.harita.set_marker(v["benim_koor"][0], v["benim_koor"][1], text="Sen")
            self.harita.set_marker(v["hedef_koor"][0], v["hedef_koor"][1], text=sehir_kisa)
            self.harita.set_path([v["benim_koor"], v["hedef_koor"]], color="#ff3b30", width=3)
            self.harita.set_position(v["hedef_koor"][0], v["hedef_koor"][1]); self.harita.set_zoom(4)
            self.baslik.configure(text=f"📍 {sehir_kisa}")
            self.mesafe.configure(text=f"✈️ Şu anki konumundan uzaklık: {v['mesafe']} km")
            
            if url:
                try:
                    img = Image.open(BytesIO(requests.get(url, timeout=5).content))
                    self.foto.configure(image=ctk.CTkImage(img, size=(410, 220)))
                    self.foto.pack(fill="x", pady=10, before=self.baslik)
                except: pass

            self.rehber_ozet.configure(text=r.get("ozet", ""))
            self.rehber_yerler.configure(text="\n".join([f"📸 {y}" for y in r.get("yerler", [])]))

            for w in self.biletler.winfo_children(): w.destroy()
            if blt:
                for b in blt:
                    krt = ctk.CTkButton(self.biletler, text=f"🛫 {b['firma']}  |  {b['fiyat']}", fg_color="#2c2c2e", height=45, command=lambda l=b['link']: webbrowser.open(l))
                    krt.pack(fill="x", pady=2)
            else:
                ctk.CTkLabel(self.biletler, text="Uygun uçuş bulunamadı.", text_color="#ff453a").pack(pady=10)
