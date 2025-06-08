class HammingLogic:
   """Hamming SEC-DED kodlama ve hata duzeltme mantigi"""

   @staticmethod
   def calculate_parity_bits(data_length):
       """Gereken parity bit sayisini hesaplar"""
       # 2^r >= m + r + 1 formulu
       r = 0
       while (2 ** r) < (data_length + r + 1):
           r += 1
       return r

   @staticmethod
   def get_parity_positions(r):
       """Parity bit pozisyonlarini dondurur: 1, 2, 4, 8, ..."""
       return [2 ** i for i in range(r)]

   @staticmethod
   def encode_data(data):
       """Veriyi Hamming SEC-DED ile kodlar"""
       m = len(data)  # Veri bit sayisi
       r = HammingLogic.calculate_parity_bits(m)
       total_length = m + r + 1  # +1 overall parity icin

       # Kodlanmis veri dizisi
       encoded_bits = ['0'] * total_length
       parity_positions = HammingLogic.get_parity_positions(r)
       overall_parity_pos = total_length

       # Veri bitlerini yerlestir (parity pozisyonlari haric)
       data_positions = []
       data_index = 0
       for i in range(1, total_length):
           if i not in parity_positions:
               encoded_bits[i - 1] = data[data_index]
               data_positions.append(i)
               data_index += 1

       # Parity bitlerini hesapla
       for parity_pos in parity_positions:
           parity_value = 0
           for i in range(1, total_length):
               if (i & parity_pos) != 0:  # AND islemi ile kontrol
                   parity_value ^= int(encoded_bits[i - 1])
           encoded_bits[parity_pos - 1] = str(parity_value)

       # Overall parity hesapla (tum bitlerin XOR'u)
       overall_parity = 0
       for bit in encoded_bits[:-1]:
           overall_parity ^= int(bit)
       encoded_bits[-1] = str(overall_parity)

       return {
           'encoded_data': ''.join(encoded_bits),
           'parity_positions': parity_positions + [overall_parity_pos],
           'data_positions': data_positions
       }

   @staticmethod
   def detect_and_correct_error(error_data, parity_positions):
       """Hata tespiti ve duzeltme yapar"""
       error_bits = list(error_data)

       # Sendrom hesapla
       syndrome = 0
       for parity_pos in parity_positions[:-1]:  # Overall parity haric
           parity_value = 0
           for j in range(1, len(error_bits) + 1):
               if (j & parity_pos) != 0:
                   parity_value ^= int(error_bits[j - 1])
           if parity_value != 0:
               syndrome += parity_pos

       # Overall parity kontrol
       overall_parity = 0
       for bit in error_bits:
           overall_parity ^= int(bit)

       # SEC-DED kurallarina gore hata durumu
       if syndrome == 0 and overall_parity == 0:
           # Hata yok
           return {
               'status': "Hata yok ✅",
               'corrected_data': error_data,
               'detected_position': "Yok",
               'corrected_positions': [],
               'syndrome': syndrome,
               'status_color': 'success'
           }

       elif syndrome == 0 and overall_parity == 1:
           # Overall parity bitinde hata
           corrected_data = list(error_data)
           corrected_data[-1] = '1' if corrected_data[-1] == '0' else '0'
           return {
               'status': "Overall parity bitinde hata - duzeltildi ✅",
               'corrected_data': ''.join(corrected_data),
               'detected_position': str(len(error_data)),
               'corrected_positions': [len(error_data)],
               'syndrome': syndrome,
               'status_color': 'success'
           }

       elif syndrome != 0 and overall_parity == 1:
           # Tek bit hatasi - duzeltebilir
           if syndrome >= 1 and syndrome <= len(error_data):
               corrected_data = list(error_data)
               corrected_data[syndrome - 1] = '1' if corrected_data[syndrome - 1] == '0' else '0'
               return {
                   'status': "Tek bit hatasi tespit edildi ve duzeltildi ✅",
                   'corrected_data': ''.join(corrected_data),
                   'detected_position': str(syndrome),
                   'corrected_positions': [syndrome],
                   'syndrome': syndrome,
                   'status_color': 'success'
               }
           else:
               # Sendrom geçersiz - bu durumda hata pozisyonu teorik olarak mümkün
               # ama pratikte kodlanmış verinin sınırları dışında
               return {
                   'status': f"Sendrom değeri {syndrome} - olası parity bit hatası ❌",
                   'corrected_data': error_data,
                   'detected_position': f"Sendrom: {syndrome} (teorik pozisyon)",
                   'corrected_positions': [],
                   'syndrome': syndrome,
                   'status_color': 'warning'
               }

       elif syndrome != 0 and overall_parity == 0:
           # Cift bit hatasi - tespit edilebilir ama duzeltilemez
           return {
               'status': "Cift bit hatasi tespit edildi (duzeltilemez) ❌",
               'corrected_data': error_data,
               'detected_position': "Belirsiz (cift hata)",
               'corrected_positions': [],
               'syndrome': syndrome,
               'status_color': 'error'
           }

       else:
           return {
               'status': "Beklenmeyen durum ❌",
               'corrected_data': error_data,
               'detected_position': "Belirsiz",
               'corrected_positions': [],
               'syndrome': syndrome,
               'status_color': 'error'
           }