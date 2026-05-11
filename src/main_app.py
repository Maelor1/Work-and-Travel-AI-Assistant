import customtkinter as ctk
from main_anaekran import AnaEkranFrame
from main_harita import HaritaFrame
from main_doviz import DovizFrame
from main_wat import WatFrame
from main_hesap import HesapFrame
from main_profil import ProfilFrame

ctk.set_appearance_mode("dark")

class AmerikaMenuluApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mali's Journey - Amerika Asistanı")
        self.geometry("1250x800")
        self.configure(fg_color="#000000") 
        self.son_aranan_sehir = "New York"
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, fg_color="#1c1c1e", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1) 
        
        ctk.CTkLabel(self.sidebar, text="✈️ MALI'S\nJOURNEY", font=("Segoe UI", 28, "bold"), text_color="#ffffff").grid(row=0, column=0, pady=50)
        
        self.btn_profil = self.menu_btn("👤 Profilim", 1, "profil")
        self.btn_ana = self.menu_btn("🏠 Ana Ekran", 2, "ana")
        self.btn_harita = self.menu_btn("🗺️ Harita & Bilet", 3, "harita")
        self.btn_doviz = self.menu_btn("💵 Döviz Çevirici", 4, "doviz")
        self.btn_hesap = self.menu_btn("💰 Bütçe Hesapla", 5, "hesap") 
        self.btn_wat = self.menu_btn("🎒 Work & Travel", 6, "wat")

        self.sayfalar = {
            "profil": ProfilFrame(self), "ana": AnaEkranFrame(self), 
            "harita": HaritaFrame(self), "doviz": DovizFrame(self), 
            "hesap": HesapFrame(self), "wat": WatFrame(self)
        }
        self.sayfa_degistir("profil")

    def menu_btn(self, text, row, sayfa):
        btn = ctk.CTkButton(self.sidebar, text=f"  {text}", font=("Segoe UI", 16, "bold"), fg_color="#1c1c1e", hover_color="#2c2c2e", text_color="#d1d1d6", anchor="w", height=45, corner_radius=10, command=lambda: self.sayfa_degistir(sayfa))
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=8)
        return btn

    def sayfa_degistir(self, sayfa):
        for btn in [self.btn_profil, self.btn_ana, self.btn_harita, self.btn_doviz, self.btn_hesap, self.btn_wat]:
            btn.configure(fg_color="#1c1c1e", text_color="#d1d1d6")
            
        aktif_butonlar = {"profil": self.btn_profil, "ana": self.btn_ana, "harita": self.btn_harita, "doviz": self.btn_doviz, "hesap": self.btn_hesap, "wat": self.btn_wat}
        aktif_butonlar[sayfa].configure(fg_color="#2c2c2e", text_color="#ffffff")

        for f in self.sayfalar.values(): f.grid_forget()
        self.sayfalar[sayfa].grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        if sayfa == "wat": self.sayfalar["wat"].ekrani_hazirla()
        if sayfa == "profil": self.sayfalar["profil"].ekrani_hazirla()

if __name__ == "__main__":
    AmerikaMenuluApp().mainloop()