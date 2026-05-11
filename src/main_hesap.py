import customtkinter as ctk
import project_delta

class HesapFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, fg_color="#000000", **kwargs)
        
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.main_scroll, text="💰 Bütçe ve Kazanç Hesaplayıcı", font=("Segoe UI", 32, "bold"), text_color="#ffffff").pack(pady=(10, 5))
        ctk.CTkLabel(self.main_scroll, text="3 aylık (12 haftalık) W&T maceranın sonunda cebinde kalacak net miktar", font=("Segoe UI", 16), text_color="#8e8e93").pack(pady=(0, 20))

        self.icerik = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.icerik.pack(fill="both", expand=True)

        # ================= SOL PANEL: İŞLER VE GİDERLER =================
        self.sol_panel = ctk.CTkFrame(self.icerik, fg_color="transparent", width=450)
        self.sol_panel.pack(side="left", fill="y", padx=(0, 10))

        # --- ANA İŞ ---
        self.is_karti(self.sol_panel, "🏦 ANA İŞ (Job 1)", "ucret1", "saat1", "#0a84ff", default_ucret=15, default_saat=40)

        # --- EK İŞLER (Checkbox ile açılır) ---
        self.check_is2 = ctk.CTkCheckBox(self.sol_panel, text="2. İşim Var", font=("Segoe UI", 14, "bold"), command=self.hesapla)
        self.check_is2.pack(pady=(10, 0), anchor="w", padx=10)
        self.is_karti(self.sol_panel, "🏢 EK İŞ", "ucret2", "saat2", "#30d158", default_ucret=12, default_saat=0)

        self.check_is3 = ctk.CTkCheckBox(self.sol_panel, text="3. İşim Var", font=("Segoe UI", 14, "bold"), command=self.hesapla)
        self.check_is3.pack(pady=(10, 0), anchor="w", padx=10)
        self.is_karti(self.sol_panel, "☕ 3. İŞ", "ucret3", "saat3", "#bf5af2", default_ucret=10, default_saat=0)

        # --- GİDERLER ---
        gider_frame = ctk.CTkFrame(self.sol_panel, fg_color="#1c1c1e", corner_radius=15)
        gider_frame.pack(fill="x", pady=15, padx=10, ipady=10)
        ctk.CTkLabel(gider_frame, text="🏠 HAFTALIK GİDERLER", font=("Segoe UI", 16, "bold"), text_color="#ff9f0a").pack(pady=5)
        
        self.lbl_kira = ctk.CTkLabel(gider_frame, text="Kira: $130", font=("Segoe UI", 14))
        self.lbl_kira.pack()
        self.slider_kira = ctk.CTkSlider(gider_frame, from_=50, to=300, command=self.hesapla, button_color="#ff9f0a")
        self.slider_kira.set(130); self.slider_kira.pack(padx=20, fill="x", pady=(0, 10))

        self.lbl_yasam = ctk.CTkLabel(gider_frame, text="Yemek/Eğlence: $120", font=("Segoe UI", 14))
        self.lbl_yasam.pack()
        self.slider_yasam = ctk.CTkSlider(gider_frame, from_=50, to=400, command=self.hesapla, button_color="#ff9f0a")
        self.slider_yasam.set(120); self.slider_yasam.pack(padx=20, fill="x")

        # ================= SAĞ PANEL: SONUÇ KARTLARI =================
        self.sag_panel = ctk.CTkFrame(self.icerik, fg_color="transparent")
        self.sag_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.kart_brut = self.bilgi_karti(self.sag_panel, "💵 3 Aylık Toplam Brüt Kazanç", "$0", "#ffffff")
        self.kart_vergi = self.bilgi_karti(self.sag_panel, "🏛️ Vergi Kesintisi (~%12)", "-$0", "#ff453a", "Sadece Federal ve State (FICA muaf)")
        self.kart_yasam = self.bilgi_karti(self.sag_panel, "🍔 Toplam Kira ve Yaşam Gideri", "-$0", "#ff9f0a", "Seçilen giderlerin 12 haftalık toplamı")
        
        ctk.CTkFrame(self.sag_panel, height=2, fg_color="#2c2c2e").pack(fill="x", pady=15, padx=20)
        self.kart_net = self.bilgi_karti(self.sag_panel, "🏦 3 AY SONUNDA CEBİNDE KALACAK NET PARA", "$0", "#30d158", boyut=36)

        self.hesapla(None)

    def is_karti(self, master, baslik, attr_ucret, attr_saat, renk, default_ucret, default_saat):
        f = ctk.CTkFrame(master, fg_color="#1c1c1e", corner_radius=15)
        f.pack(fill="x", pady=5, padx=10, ipady=5)
        ctk.CTkLabel(f, text=baslik, font=("Segoe UI", 15, "bold"), text_color=renk).pack(pady=5)
        
        setattr(self, f"lbl_{attr_ucret}", ctk.CTkLabel(f, text=f"${default_ucret}/saat", font=("Segoe UI", 13)))
        getattr(self, f"lbl_{attr_ucret}").pack()
        setattr(self, attr_ucret, ctk.CTkSlider(f, from_=8, to=35, command=self.hesapla, button_color=renk))
        getattr(self, attr_ucret).set(default_ucret); getattr(self, attr_ucret).pack(padx=20, fill="x")

        setattr(self, f"lbl_{attr_saat}", ctk.CTkLabel(f, text=f"{default_saat} Saat/Hafta", font=("Segoe UI", 13)))
        getattr(self, f"lbl_{attr_saat}").pack()
        setattr(self, attr_saat, ctk.CTkSlider(f, from_=0, to=80, command=self.hesapla, button_color=renk))
        getattr(self, attr_saat).set(default_saat); getattr(self, attr_saat).pack(padx=20, fill="x")

    def bilgi_karti(self, master, baslik, deger, renk, alt_bilgi="", boyut=24):
        kart = ctk.CTkFrame(master, fg_color="#1c1c1e", corner_radius=18)
        kart.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(kart, text=baslik, font=("Segoe UI", 16, "bold"), text_color="#d1d1d6").pack(anchor="w", padx=25, pady=(15, 0))
        if alt_bilgi: ctk.CTkLabel(kart, text=alt_bilgi, font=("Segoe UI", 12), text_color="#8e8e93").pack(anchor="w", padx=25)
        lbl = ctk.CTkLabel(kart, text=deger, font=("Segoe UI", boyut, "bold"), text_color=renk)
        lbl.pack(anchor="e", padx=25, pady=(5, 15))
        return lbl

    def hesapla(self, _=None):
        # Arayüz güncellemeleri
        self.lbl_ucret1.configure(text=f"${self.ucret1.get():.1f}/saat"); self.lbl_saat1.configure(text=f"{int(self.saat1.get())} Saat/Hafta")
        self.lbl_ucret2.configure(text=f"${self.ucret2.get():.1f}/saat"); self.lbl_saat2.configure(text=f"{int(self.saat2.get())} Saat/Hafta")
        self.lbl_ucret3.configure(text=f"${self.ucret3.get():.1f}/saat"); self.lbl_saat3.configure(text=f"{int(self.saat3.get())} Saat/Hafta")
        self.lbl_kira.configure(text=f"Kira: ${int(self.slider_kira.get())}"); self.lbl_yasam.configure(text=f"Yemek/Eğlence: ${int(self.slider_yasam.get())}")

        # Matematik
        kazanc1 = self.ucret1.get() * self.saat1.get()
        kazanc2 = (self.ucret2.get() * self.saat2.get()) if self.check_is2.get() else 0
        kazanc3 = (self.ucret3.get() * self.saat3.get()) if self.check_is3.get() else 0
        
        brut_3ay = (kazanc1 + kazanc2 + kazanc3) * 12
        vergi = brut_3ay * 0.12 
        gider_3ay = (self.slider_kira.get() + self.slider_yasam.get()) * 12
        net = brut_3ay - vergi - gider_3ay

        # Kartlara Yazdır ve Profile Gönder
        self.kart_brut.configure(text=f"${brut_3ay:,.0f}")
        self.kart_vergi.configure(text=f"-${vergi:,.0f}")
        self.kart_yasam.configure(text=f"-${gider_3ay:,.0f}")
        self.kart_net.configure(text=f"${net:,.0f}", text_color="#30d158" if net >= 0 else "#ff453a")
        project_delta.db_yaz("beklenen_net_kazanc", net)