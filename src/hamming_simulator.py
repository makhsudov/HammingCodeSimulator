import tkinter as tk
from tkinter import messagebox
import random
from config import COLORS, STYLES
from hamming_logic import HammingLogic


class HammingSECDEDSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming SEC-DED Code Simulatoru")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Ana arayuz ve degiskenleri kurulum
        self.setup_ui()
        self.init_variables()
        self.on_size_change()

    def setup_ui(self):
        """Ana arayuz bilesenlerini olustur ve duzenle"""
        self.root.configure(bg=COLORS['bg'])

        # Ana cerceve olustur ve ekrana yerlestir
        main_frame = tk.Frame(self.root, bg=COLORS['bg'],
                              padx=STYLES['padding'], pady=STYLES['padding'])
        main_frame.pack(fill='both', expand=True)

        # Sirasiyla tum bolumler icin arayuz olustur
        self.create_color_explanation(main_frame)  # Renk aciklamasi bolumu
        self.create_size_selection(main_frame)     # Veri boyutu secim bolumu
        self.create_input_section(main_frame)      # Veri giris bolumu
        self.create_encoding_section(main_frame)   # Kodlama sonuc bolumu
        self.create_error_section(main_frame)      # Hata simulasyon bolumu
        self.create_correction_section(main_frame) # Hata duzeltme bolumu

    def create_color_explanation(self, parent):
        """Renklerin ne anlama geldigini gosteren aciklama bolumu"""
        # Renk aciklama cercevesi olustur
        explanation_frame = tk.LabelFrame(parent, text="Renk Aciklamasi",
                                     bg=COLORS['bg'], fg=COLORS['label_fg'],
                                     font=STYLES['section_font'])
        explanation_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'], ipady=3)

        # Icinde renk orneklerini gosterecek cerceve
        explanation_inner = tk.Frame(explanation_frame, bg=COLORS['bg'])
        explanation_inner.pack(pady=STYLES['small_padding'])

        # Her bit tipi icin renk ve aciklama listesi
        color_explanations = [
            ("Veri Bitleri", COLORS['data_bit']),        # Asil veri bitleri
            ("Parity Bitleri", COLORS['parity_bit']),    # Hata kontrol bitleri
            ("Overall Parity", COLORS['overall_parity']), # Genel parity biti
            ("Hata Bitleri", COLORS['error_bit'])         # Hatali olan bitler
        ]

        # Her renk icin aciklama ve ornek olustur
        for text, color in color_explanations:
            # Her bir renk ornegi icin mini cerceve
            explanation_item = tk.Frame(explanation_inner, bg=COLORS['bg'])
            explanation_item.pack(side='left', padx=(0, 15))

            # Rengi gosteren renkli blok (kare sembol)
            color_box = tk.Label(explanation_item, text="██", fg=color, bg=COLORS['bg'],
                                 font=STYLES['bit_font'])
            color_box.pack(side='left')

            # Rengin ne oldugunu anlatan yazi
            tk.Label(explanation_item, text=text, bg=COLORS['bg'],
                     fg=COLORS['label_fg'], font=STYLES['normal_font']).pack(side='left', padx=(5, 0))

    def create_size_selection(self, parent):
        """Veri boyutu secimi icin radio butonlar"""
        # Boyut secim cercevesi
        size_frame = tk.LabelFrame(parent, text="Veri Boyutu",
                                   bg=COLORS['bg'], fg=COLORS['label_fg'],
                                   font=STYLES['section_font'])
        size_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'], ipady=3)

        # Varsayilan olarak 8 bit secili
        self.data_size = tk.StringVar(value="8")

        # Radio butonlari icin cerceve
        radio_frame = tk.Frame(size_frame, bg=COLORS['bg'])
        radio_frame.pack(pady=STYLES['small_padding'])

        # 8, 16, 32 bit secenekleri icin radio butonlar
        for size, text in [("8", "8 bit"), ("16", "16 bit"), ("32", "32 bit")]:
            tk.Radiobutton(radio_frame, text=text, variable=self.data_size, value=size,
                           command=self.on_size_change, bg=COLORS['bg'],
                           fg=COLORS['label_fg'], selectcolor=COLORS['frame_bg'],
                           font=STYLES['normal_font'], activebackground=COLORS['bg'],
                           activeforeground=COLORS['fg']).pack(side='left', padx=(0, 20))

    def create_input_section(self, parent):
        """Kullanicinin binary veri girecegi bolum"""
        # Ana veri giris cercevesi
        input_frame = tk.Frame(parent, bg=COLORS['bg'])
        input_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'])

        # Baslik ve rastgele veri butonu icin ust kisim
        header = tk.Frame(input_frame, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, STYLES['small_padding']))

        # Sol tarafta bolum basligi
        tk.Label(header, text="Veri Girisi", bg=COLORS['bg'],
                 fg=COLORS['label_fg'], font=STYLES['section_font']).pack(side='left')

        # Sag tarafta rastgele veri olusturan buton
        tk.Button(header, text="Rastgele Veri Olustur", bg=COLORS['button_bg'],
                  fg=COLORS['button_fg'], font=STYLES['normal_font'],
                  activebackground=COLORS['button_active'], relief=STYLES['button_relief'],
                  command=self.generate_random_data).pack(side='right')

        # Veri giris alanini iceren cerceve
        content = tk.Frame(input_frame, bg=COLORS['frame_bg'],
                           relief=STYLES['frame_relief'], bd=STYLES['frame_border'])
        content.pack(fill='x', padx=2, pady=2, ipady=5)

        # Text input alani icin ic cerceve
        input_inner = tk.Frame(content, bg=COLORS['frame_bg'])
        input_inner.pack(fill='x', pady=STYLES['small_padding'], padx=STYLES['small_padding'])

        # "Veri (Binary):" etiketi
        tk.Label(input_inner, text="Veri (Binary):", bg=COLORS['frame_bg'],
                 fg=COLORS['label_fg'], font=STYLES['normal_font']).pack(side='left')

        # Binary veri giris kutusu - sadece 0 ve 1 kabul eder
        self.data_entry = tk.Entry(input_inner, width=35, bg=COLORS['entry_bg'],
                                   fg=COLORS['entry_fg'], font=STYLES['mono_font'],
                                   insertbackground=COLORS['entry_fg'])
        self.data_entry.pack(side='left', padx=(10, 10))
        # Her tus basin da validasyon kontolu yap
        self.data_entry.bind('<KeyRelease>', self.validate_input)

    def create_encoding_section(self, parent):
        """Hamming kodlama sonuclarini gosteren bolum"""
        # Kodlama sonuclari cercevesi
        encode_frame = tk.Frame(parent, bg=COLORS['bg'])
        encode_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'])

        # Baslik ve kodlama butonu
        header = tk.Frame(encode_frame, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, STYLES['small_padding']))

        # Bolum basligi
        tk.Label(header, text="Kodlama Sonuclari", bg=COLORS['bg'],
                 fg=COLORS['label_fg'], font=STYLES['section_font']).pack(side='left')

        # Kodlama islemini baslatan buton
        tk.Button(header, text="Kodla", bg=COLORS['button_bg'],
                  fg=COLORS['button_fg'], font=STYLES['normal_font'],
                  activebackground=COLORS['button_active'], relief=STYLES['button_relief'],
                  command=self.encode_data).pack(side='right')

        # Kodlama sonuclarini gosteren icerik alani
        content = tk.Frame(encode_frame, bg=COLORS['frame_bg'],
                           relief=STYLES['frame_relief'], bd=STYLES['frame_border'])
        content.pack(fill='x', padx=2, pady=2, ipady=5)

        # Sonuc satirlari olustur
        self.create_info_row(content, "Orijinal Veri:", 'original_label')      # Girilen ham veri
        self.create_colored_info_row(content, "Hamming Kodu:", 'encoded_frame') # Renkli kodlanmis veri
        self.create_info_row(content, "Parity Bitleri:", 'parity_label')       # Parity bit bilgileri

    def create_error_section(self, parent):
        """Hata simulasyonu yapilan bolum"""
        # Hata simulasyon cercevesi
        error_frame = tk.Frame(parent, bg=COLORS['bg'])
        error_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'])

        # Baslik ve hata butonlari
        header = tk.Frame(error_frame, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, STYLES['small_padding']))

        # Bolum basligi
        tk.Label(header, text="Hata Simulasyonu", bg=COLORS['bg'],
                 fg=COLORS['label_fg'], font=STYLES['section_font']).pack(side='left')

        # Rastgele pozisyonda hata ureten buton
        tk.Button(header, text="Rastgele Hata", bg=COLORS['button_bg'],
                  fg=COLORS['button_fg'], font=STYLES['normal_font'],
                  activebackground=COLORS['button_active'], relief=STYLES['button_relief'],
                  command=self.generate_random_error).pack(side='right', padx=(5, 0))

        # Belirli pozisyonda hata olusturan buton
        tk.Button(header, text="Hata Olustur", bg=COLORS['button_bg'],
                  fg=COLORS['button_fg'], font=STYLES['normal_font'],
                  activebackground=COLORS['button_active'], relief=STYLES['button_relief'],
                  command=self.introduce_error).pack(side='right')

        # Hata giris ve sonuc alani
        content = tk.Frame(error_frame, bg=COLORS['frame_bg'],
                           relief=STYLES['frame_relief'], bd=STYLES['frame_border'])
        content.pack(fill='x', padx=2, pady=2, ipady=5)

        # Hata pozisyonu giris alani
        error_input_frame = tk.Frame(content, bg=COLORS['frame_bg'])
        error_input_frame.pack(fill='x', pady=2, padx=STYLES['small_padding'])

        # Hata pozisyonu etiketi
        tk.Label(error_input_frame, text="Hata Bit Pozisyonu:", bg=COLORS['frame_bg'],
                 fg=COLORS['label_fg'], font=STYLES['normal_font']).pack(side='left')

        # Pozisyon giris kutusu
        self.error_pos_var = tk.StringVar()
        self.error_entry = tk.Entry(error_input_frame, textvariable=self.error_pos_var, width=10,
                                    bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                                    font=STYLES['mono_font'], insertbackground=COLORS['entry_fg'])
        self.error_entry.pack(side='left', padx=(10, 10))

        # Hatali veriyi renkli gosteren satir
        self.create_colored_info_row(content, "Hatali Veri:", 'error_frame')

    def create_correction_section(self, parent):
        """Hata tespiti ve duzeltme sonuclarini gosteren bolum"""
        # Duzeltme cercevesi
        correction_frame = tk.Frame(parent, bg=COLORS['bg'])
        correction_frame.pack(fill='x', pady=(0, 8), padx=STYLES['small_padding'])

        # Baslik ve duzeltme butonu
        header = tk.Frame(correction_frame, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, STYLES['small_padding']))

        # Bolum basligi
        tk.Label(header, text="Hata Tespiti ve Duzeltme", bg=COLORS['bg'],
                 fg=COLORS['label_fg'], font=STYLES['section_font']).pack(side='left')

        # Hata tespit ve duzeltme islemini baslatan buton
        tk.Button(header, text="Hata Tespit Et ve Duzelt", bg=COLORS['button_bg'],
                  fg=COLORS['button_fg'], font=STYLES['normal_font'],
                  activebackground=COLORS['button_active'], relief=STYLES['button_relief'],
                  command=self.detect_and_correct).pack(side='right')

        # Duzeltme sonuclarini gosteren icerik alani
        content = tk.Frame(correction_frame, bg=COLORS['frame_bg'],
                           relief=STYLES['frame_relief'], bd=STYLES['frame_border'])
        content.pack(fill='x', padx=2, pady=2, ipady=5)

        # Duzeltme sonuc satirlari
        self.create_info_row(content, "Sendrom:", 'syndrome_label')                    # Hata sendromu
        self.create_info_row(content, "Tespit Edilen Hata Pozisyonu:", 'detected_error_label') # Bulunan hata yeri
        self.create_colored_info_row(content, "Duzeltilmis Veri:", 'corrected_frame')  # Duzeltilmis veri
        self.create_info_row(content, "Durum:", 'status_label', is_status=True)        # Islem durumu

    def create_info_row(self, parent, label_text, attr_name, is_status=False):
        """Tek satirlik bilgi gosteren widget grubu olustur"""
        # Satir cercevesi
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill='x', pady=1, padx=STYLES['small_padding'])

        # Sol tarafta etiket
        tk.Label(frame, text=label_text, bg=COLORS['frame_bg'],
                 fg=COLORS['label_fg'], font=STYLES['normal_font'],
                 width=20, anchor='w').pack(side='left')

        # Sag tarafta deger gosteren label
        if is_status:
            # Durum mesajlari icin farkli stil
            label = tk.Label(frame, text="", bg=COLORS['frame_bg'],
                             fg=COLORS['success'], font=STYLES['section_font'], anchor='w')
        else:
            # Normal bilgi icin monospace font
            label = tk.Label(frame, text="", bg=COLORS['frame_bg'],
                             fg=COLORS['fg'], font=STYLES['mono_font'], anchor='w')

        label.pack(side='left', fill='x', expand=True)
        # Bu label'i sinif degiskeni olarak kaydet
        setattr(self, attr_name, label)

    def create_colored_info_row(self, parent, label_text, attr_name):
        """Renkli bit gosterimi icin ozel satir olustur"""
        # Satir cercevesi
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill='x', pady=1, padx=STYLES['small_padding'])

        # Sol tarafta etiket
        tk.Label(frame, text=label_text, bg=COLORS['frame_bg'],
                 fg=COLORS['label_fg'], font=STYLES['normal_font'],
                 width=20, anchor='w').pack(side='left')

        # Sag tarafta renkli bitleri barindiran cerceve
        colored_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        colored_frame.pack(side='left', fill='x', expand=True)
        # Bu cerceve'yi sinif degiskeni olarak kaydet
        setattr(self, attr_name, colored_frame)

    def display_colored_bits(self, frame, data, bit_types=None, error_positions=None):
        """Bit dizisini renkli olarak goster"""
        # Onceki gosterimi temizle
        for widget in frame.winfo_children():
            widget.destroy()

        # Veri yoksa islem yapma
        if not data:
            return

        # Her bit icin renkli label olustur
        for i, bit in enumerate(data):
            position = i + 1  # 1'den baslayan pozisyon numarasi
            color = COLORS['fg']  # Varsayilan renk

            # Bit tipine gore renk belirle
            if bit_types:
                if position in bit_types.get('parity', []):
                    color = COLORS['parity_bit']           # Parity bitleri
                elif position == bit_types.get('overall_parity', 0):
                    color = COLORS['overall_parity']       # Genel parity biti
                elif position in bit_types.get('data', []):
                    color = COLORS['data_bit']             # Veri bitleri

            # Hata pozisyonlari varsa onlari vurgula
            if error_positions and position in error_positions:
                color = COLORS['error_bit']

            # Tek bit icin renkli label olustur
            bit_label = tk.Label(frame, text=bit, fg=color, bg=COLORS['frame_bg'],
                                 font=STYLES['bit_font'])
            bit_label.pack(side='left', padx=(0, 2))  # Yan yana diz, arada bosluk birak

    def init_variables(self):
        """Baslangic degiskenlerini sifirla"""
        self.original_data = ""      # Orijinal girilen veri
        self.encoded_data = ""       # Hamming kodlu veri
        self.error_data = ""         # Hatali veri
        self.parity_positions = []   # Parity bit pozisyonlari
        self.data_positions = []     # Veri bit pozisyonlari
        self.error_position = None   # Hata pozisyonu

    def on_size_change(self):
        """Veri boyutu degistiginde gerekli temizlik ve reset islemleri"""
        size = int(self.data_size.get())
        # Veri giris kutusunu temizle
        self.data_entry.delete(0, tk.END)
        # Secilen boyutta sifir dizisi yerlestir
        placeholder = "0" * size
        self.data_entry.insert(0, placeholder)
        # Tum sonuclari temizle
        self.clear_all_results()

    def validate_input(self, event=None):
        """Veri giris kutusunda sadece 0 ve 1 karakterlerine izin ver"""
        data = self.data_entry.get()
        size = int(self.data_size.get())

        # Sadece 0 ve 1 karakterlerini al
        valid_data = ''.join(c for c in data if c in '01')

        # Boyut sinirini kontrol et
        if len(valid_data) > size:
            valid_data = valid_data[:size]

        # Eger veri degistiyse kutuyu guncelle
        if data != valid_data:
            current_pos = self.data_entry.index(tk.INSERT)  # Cursor pozisyonu
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, valid_data)
            # Cursor pozisyonunu korumaya calis
            try:
                self.data_entry.icursor(min(current_pos, len(valid_data)))
            except:
                pass

    def generate_random_data(self):
        """Secilen boyutta rastgele binary veri olustur"""
        size = int(self.data_size.get())
        # Her pozisyon icin rastgele 0 veya 1 sec
        random_data = ''.join(random.choice('01') for _ in range(size))
        # Veri kutusunu guncelle
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, random_data)
        # Onceki sonuclari temizle
        self.clear_all_results()

    def encode_data(self):
        """Girilen veriyi Hamming SEC-DED koduyla kodla"""
        data = self.data_entry.get().strip()
        # Veri kontrolu
        if not data:
            messagebox.showerror("Hata", "Lutfen veri girin!")
            return

        size = int(self.data_size.get())
        if len(data) != size:
            messagebox.showerror("Hata", f"Veri {size} bit olmalidir!")
            return

        # Veriyi kaydet
        self.original_data = data

        # Hamming Logic sinifini kullanarak kodla
        result = HammingLogic.encode_data(data)
        self.encoded_data = result['encoded_data']
        self.parity_positions = result['parity_positions']
        self.data_positions = result['data_positions']

        # Kodlama sonuclarini ekranda goster
        self.original_label.config(text=self.original_data)

        # Bit tiplerini belirle ve renkli goster
        bit_types = {
            'data': self.data_positions,
            'parity': self.parity_positions[:-1],      # Son haric parity bitleri
            'overall_parity': self.parity_positions[-1] # Son bit overall parity
        }
        self.display_colored_bits(self.encoded_frame, self.encoded_data, bit_types)

        # Parity bit bilgilerini metin olarak goster
        parity_info = f"Pozisyonlar: {self.parity_positions}, Degerler: "
        parity_values = [self.encoded_data[pos - 1] for pos in self.parity_positions]
        parity_info += ''.join(parity_values)
        self.parity_label.config(text=parity_info)

        # Hata bolumunu temizle
        self.clear_error_results()

    def generate_random_error(self):
        """Rastgele bir pozisyonda hata olusturmak icin pozisyon belirle"""
        if not self.encoded_data:
            messagebox.showerror("Hata", "Once veriyi kodlayin!")
            return

        # 1 ile veri uzunlugu arasinda rastgele pozisyon sec
        error_pos = random.randint(1, len(self.encoded_data))
        self.error_pos_var.set(str(error_pos))

        # Hatali veri gorselini temizle
        self.error_data = ""
        self.error_position = None
        for widget in self.error_frame.winfo_children():
            widget.destroy()
        self.clear_correction_results()

    def introduce_error(self):
        """Belirtilen pozisyonda bit hatasi olustur"""
        if not self.encoded_data:
            messagebox.showerror("Hata", "Once veriyi kodlayin!")
            return

        # Hata pozisyonunu al ve kontrol et
        try:
            error_pos = int(self.error_pos_var.get())
            if error_pos < 1 or error_pos > len(self.encoded_data):
                messagebox.showerror("Hata", f"Hata pozisyonu 1-{len(self.encoded_data)} arasinda olmalidir!")
                return
        except ValueError:
            messagebox.showerror("Hata", "Gecerli bir pozisyon girin!")
            return

        # Belirtilen pozisyondaki biti ters cevir (0->1, 1->0)
        error_bits = list(self.encoded_data)
        error_bits[error_pos - 1] = '1' if error_bits[error_pos - 1] == '0' else '0'
        self.error_data = ''.join(error_bits)
        self.error_position = error_pos

        # Hatali veriyi renkli goster, hata pozisyonu vurgulansin
        bit_types = {
            'data': self.data_positions,
            'parity': self.parity_positions[:-1],
            'overall_parity': self.parity_positions[-1]
        }
        self.display_colored_bits(self.error_frame, self.error_data, bit_types, [error_pos])

        # Duzeltme sonuclarini temizle
        self.clear_correction_results()

    def detect_and_correct(self):
        """Hatali veride hata tespiti ve duzeltme yap"""
        if not self.error_data:
            messagebox.showerror("Hata", "Once hata olusturun!")
            return

        # Hamming Logic ile hata tespit ve duzelt
        result = HammingLogic.detect_and_correct_error(self.error_data, self.parity_positions)

        # Bit tiplerini belirle
        bit_types = {
            'data': self.data_positions,
            'parity': self.parity_positions[:-1],
            'overall_parity': self.parity_positions[-1]
        }

        # Eger duzeltme yapildiysa duzeltilen pozisyonlari yesil goster
        if result['corrected_positions']:
            # Onceki gosterimi temizle
            for widget in self.corrected_frame.winfo_children():
                widget.destroy()

            # Her bit icin label olustur
            for i, bit in enumerate(result['corrected_data']):
                position = i + 1
                color = COLORS['fg']

                # Normal bit rengini belirle
                if position in bit_types.get('parity', []):
                    color = COLORS['parity_bit']
                elif position == bit_types.get('overall_parity', 0):
                    color = COLORS['overall_parity']
                elif position in bit_types.get('data', []):
                    color = COLORS['data_bit']

                # Duzeltilen pozisyonlari yesil yap
                if position in result['corrected_positions']:
                    color = COLORS['success']

                # Bit label'ini olustur ve yerlestir
                bit_label = tk.Label(self.corrected_frame, text=bit, fg=color,
                                     bg=COLORS['frame_bg'], font=STYLES['bit_font'])
                bit_label.pack(side='left', padx=(0, 2))
        else:
            # Duzeltme yoksa normal renkli gosterim
            self.display_colored_bits(self.corrected_frame, result['corrected_data'], bit_types)

        # Hata tespit sonuclarini goster
        # Sendromu binary ve decimal olarak goster
        syndrome_binary = bin(result['syndrome'])[2:].zfill(len(self.parity_positions) - 1)
        self.syndrome_label.config(text=f"{syndrome_binary} (decimal: {result['syndrome']})")
        # Tespit edilen hata pozisyonu
        self.detected_error_label.config(text=result['detected_position'])
        # Genel durum mesaji (basarili/basarisiz)
        self.status_label.config(text=result['status'], fg=COLORS[result['status_color']])

    def clear_all_results(self):
        """Tum sonuc alanlarini temizle"""
        self.original_label.config(text="")
        # Renkli bit gosterimlerini temizle
        for widget in self.encoded_frame.winfo_children():
            widget.destroy()
        self.parity_label.config(text="")
        self.clear_error_results()

    def clear_error_results(self):
        """Hata ile ilgili tum sonuclari temizle"""
        for widget in self.error_frame.winfo_children():
            widget.destroy()
        self.error_pos_var.set("")
        self.clear_correction_results()

    def clear_correction_results(self):
        """Hata duzeltme sonuclarini temizle"""
        self.syndrome_label.config(text="")
        self.detected_error_label.config(text="")
        for widget in self.corrected_frame.winfo_children():
            widget.destroy()
        self.status_label.config(text="")