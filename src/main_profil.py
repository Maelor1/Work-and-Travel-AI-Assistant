import customtkinter as ctk
import project_delta

class ProfilFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, fg_color="#000000", **kwargs)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

    def ekrani_hazirla(self):
        for w in self.scroll.winfo_children(): w.destroy()

        # --- BÜTÇE KARTI ---
        ust_kart = ctk.CTkFrame(self.scroll, fg_color="#1c1c1e", corner_radius=25)
        ust_kart.pack(fill="x", pady=(0, 20), ipady=15)
        ctk.CTkLabel(ust_kart, text="💰 Tahmini Net Birikim", font=("Segoe UI", 16), text_color="#8e8e93").pack(pady=(15, 0))
        net_para = project_delta.db_oku("beklenen_net_kazanc") or 0
        ctk.CTkLabel(ust_kart, text=f"${net_para:,.0f}", font=("Segoe UI", 48, "bold"), text_color="#30d158").pack()

        # --- ÇALIŞMA YERLERİM  ---
        is_frame = ctk.CTkFrame(self.scroll, fg_color="#1c1c1e", corner_radius=25)
        is_frame.pack(fill="x", pady=10, ipady=15)
        ctk.CTkLabel(is_frame, text="🏢 Çalışma Yerlerim", font=("Segoe UI", 20, "bold"), text_color="#0a84ff").pack(anchor="w", padx=25, pady=10)

        self.is_satiri_olustur(is_frame, "is1", "1. İş Yeri")
        self.is_satiri_olustur(is_frame, "is2", "2. İş Yeri")
        self.is_satiri_olustur(is_frame, "is3", "3. İş Yeri")

        # --- SEYAHAT ROTASI VE DETAYLI DEĞERLENDİRME ---
        ctk.CTkLabel(self.scroll, text="🗺️ Seyahat Günlüğüm", font=("Segoe UI", 22, "bold"), text_color="#ffffff").pack(anchor="w", pady=(25, 10), padx=10)
        sehirler = project_delta.db_oku("aranan_sehirler") or {}
        
        if not sehirler:
            ctk.CTkLabel(self.scroll, text="Haritada arattığın şehirler burada listelenecek... 🧭", font=("Segoe UI", 15), text_color="#48484a").pack(pady=20)
        else:
            for sehir, veri in sehirler.items():
                self.sehir_karti_olustur(sehir, veri)

    def is_satiri_olustur(self, master, db_key, baslik):
        mevcut_isim = project_delta.db_oku(db_key) or ""
        
        satir = ctk.CTkFrame(master, fg_color="transparent")
        satir.pack(fill="x", padx=20, pady=8)

        if mevcut_isim:
            gosterim = f"{baslik}: {mevcut_isim}"
            renk = "#ffffff"
        else:
            gosterim = f"{baslik}: (Eklenmedi)"
            renk = "#8e8e93"

        lbl = ctk.CTkLabel(satir, text=gosterim, font=("Segoe UI", 16), text_color=renk)
        lbl.pack(side="left", padx=10)

        def sil():
            project_delta.db_yaz(db_key, "")
            self.ekrani_hazirla()

        def duzenle():
            for w in satir.winfo_children(): w.destroy()
            
            ctk.CTkLabel(satir, text=f"{baslik}:", font=("Segoe UI", 16), text_color="#8e8e93").pack(side="left", padx=10)
            entry = ctk.CTkEntry(satir, width=250, height=35, corner_radius=10, font=("Segoe UI", 15))
            entry.insert(0, mevcut_isim)
            entry.pack(side="left", padx=10)
            
            def kaydet():
                project_delta.db_yaz(db_key, entry.get().strip())
                self.ekrani_hazirla()
            
            ctk.CTkButton(satir, text="✔️ Kaydet", font=("Segoe UI", 14, "bold"), width=80, height=35, command=kaydet, fg_color="#30d158", hover_color="#28ad48").pack(side="left", padx=5)
            ctk.CTkButton(satir, text="❌ İptal", font=("Segoe UI", 14, "bold"), width=80, height=35, command=self.ekrani_hazirla, fg_color="#ff453a", hover_color="#cc372e").pack(side="left", padx=5)

        if mevcut_isim:
            ctk.CTkButton(satir, text="❌", width=35, height=35, fg_color="#ff453a", hover_color="#cc372e", command=sil, corner_radius=8).pack(side="right", padx=5)
        ctk.CTkButton(satir, text="✎", width=35, height=35, fg_color="#2c2c2e", text_color="#0a84ff", hover_color="#3a3a3c", command=duzenle, corner_radius=8).pack(side="right", padx=5)

    def sehir_karti_olustur(self, sehir, veri):
        kart = ctk.CTkFrame(self.scroll, fg_color="#1c1c1e", corner_radius=15)
        kart.pack(fill="x", pady=8, ipady=10, padx=5)
        
        # --- ÜST SATIR (İsim ve Durum) ---
        ust_satir = ctk.CTkFrame(kart, fg_color="transparent")
        ust_satir.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(ust_satir, text=f"📍 {sehir}", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)
        
        def sil():
            s = project_delta.db_oku("aranan_sehirler")
            if sehir in s: del s[sehir]
            project_delta.db_yaz("aranan_sehirler", s); self.ekrani_hazirla()
            
        ctk.CTkButton(ust_satir, text="❌ Sil", width=60, fg_color="#ff453a", hover_color="#cc372e", command=sil).pack(side="right", padx=10)

        def durum_degis(yeni):
            s = project_delta.db_oku("aranan_sehirler")
            s[sehir]["durum"] = yeni
            # Yeni duruma geçerken eğer "puanlar" sözlüğü yoksa oluştur
            if "puanlar" not in s[sehir]:
                s[sehir]["puanlar"] = {"ortam": "⭐⭐⭐⭐⭐", "aktivite": "⭐⭐⭐⭐⭐", "temizlik": "⭐⭐⭐⭐⭐", "fiyat": "💲💲💲"}
            project_delta.db_yaz("aranan_sehirler", s)
            self.ekrani_hazirla()

        m = ctk.CTkOptionMenu(ust_satir, values=["Gitmedim", "Planlıyorum", "Gittim"], command=durum_degis, fg_color="#2c2c2e", width=140)
        m.set(veri.get("durum", "Planlıyorum")); m.pack(side="right", padx=10)

        # --- ALT SATIR (Detaylı Puanlama Tablosu - SADECE GİTTİYSE) ---
        if veri.get("durum") == "Gittim":
            alt_satir = ctk.CTkFrame(kart, fg_color="#2c2c2e", corner_radius=10)
            alt_satir.pack(fill="x", padx=20, pady=(10, 5), ipady=5)
            
            puanlar = veri.get("puanlar", {"ortam": "⭐⭐⭐⭐⭐", "aktivite": "⭐⭐⭐⭐⭐", "temizlik": "⭐⭐⭐⭐⭐", "fiyat": "💲💲💲"})
            
            def p_degis(kategori, deger):
                s = project_delta.db_oku("aranan_sehirler")
                if "puanlar" not in s[sehir]: s[sehir]["puanlar"] = {}
                s[sehir]["puanlar"][kategori] = deger
                project_delta.db_yaz("aranan_sehirler", s)

            sol_sutun = ctk.CTkFrame(alt_satir, fg_color="transparent")
            sol_sutun.pack(side="left", expand=True, fill="both", padx=10)
            
            sag_sutun = ctk.CTkFrame(alt_satir, fg_color="transparent")
            sag_sutun.pack(side="right", expand=True, fill="both", padx=10)

            # 1. Ortam & İnsanlar
            f1 = ctk.CTkFrame(sol_sutun, fg_color="transparent"); f1.pack(fill="x", pady=5)
            ctk.CTkLabel(f1, text="👯‍♂️ Ortam & İnsanlar:", font=("Segoe UI", 14)).pack(side="left")
            m1 = ctk.CTkOptionMenu(f1, values=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], command=lambda p: p_degis("ortam", p), width=80, fg_color="#ffd60a", text_color="#000000")
            m1.set(puanlar.get("ortam", "⭐⭐⭐⭐⭐")); m1.pack(side="right")

            # 2. Aktivite & Eğlence
            f2 = ctk.CTkFrame(sol_sutun, fg_color="transparent"); f2.pack(fill="x", pady=5)
            ctk.CTkLabel(f2, text="🎢 Aktivite & Eğlence:", font=("Segoe UI", 14)).pack(side="left")
            m2 = ctk.CTkOptionMenu(f2, values=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], command=lambda p: p_degis("aktivite", p), width=80, fg_color="#ffd60a", text_color="#000000")
            m2.set(puanlar.get("aktivite", "⭐⭐⭐⭐⭐")); m2.pack(side="right")

            # 3. Temizlik & Güvenlik
            f3 = ctk.CTkFrame(sag_sutun, fg_color="transparent"); f3.pack(fill="x", pady=5)
            ctk.CTkLabel(f3, text="✨ Temizlik & Güvenlik:", font=("Segoe UI", 14)).pack(side="left")
            m3 = ctk.CTkOptionMenu(f3, values=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], command=lambda p: p_degis("temizlik", p), width=80, fg_color="#ffd60a", text_color="#000000")
            m3.set(puanlar.get("temizlik", "⭐⭐⭐⭐⭐")); m3.pack(side="right")

            # 4. Fiyat (Öğrenci Dostu) -> Dolar Sembolü
            f4 = ctk.CTkFrame(sag_sutun, fg_color="transparent"); f4.pack(fill="x", pady=5)
            ctk.CTkLabel(f4, text="💸 Pahalılık Seviyesi:", font=("Segoe UI", 14)).pack(side="left")
            m4 = ctk.CTkOptionMenu(f4, values=["💲", "💲💲", "💲💲💲", "💲💲💲💲", "💲💲💲💲💲"], command=lambda p: p_degis("fiyat", p), width=80, fg_color="#30d158", text_color="#000000")
            m4.set(puanlar.get("fiyat", "💲💲💲")); m4.pack(side="right")
