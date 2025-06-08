import tkinter as tk
from hamming_simulator import HammingSECDEDSimulator

if __name__ == "__main__":

    """Uygulamanin baslatildigi ana fonksiyon"""
    print("Hamming SEC-DED Code Simulatoru baslatiliyor...")
    print("=" * 50)
    print("Proje:     Hamming SEC-DED Code Simulatoru")
    print("Ad Soyad:  Edem Makhsudov")
    print("Ogr No:    22360859373")
    print("GUI:       Python Tkinter")
    print("=" * 50)
    root = tk.Tk()
    app = HammingSECDEDSimulator(root)
    root.mainloop()