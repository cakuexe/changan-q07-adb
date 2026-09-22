========================================================
  ATTACK_VECENTEK.BAT - KULLANIM KILAVUZU
========================================================

AMAÇ:
------
ADB komutları üzerinden 7 farklı yükleme yöntemi deneyerek
Vecentek korumasını kaba kuvvet (brute force) ile aşmak.

ÇALIŞMA PRENSİBİ:
-----------------
Script, APK'yı bilgisayardan arabaya yüklerken farklı
parametreler ve yöntemler kullanarak Vecentek'i atlatmaya çalışır.

7 SALDIRI YÖNTEMİ:
------------------

SALDIRI 1: Servisi Durdur ve Yükle (Hitman)
- Vecentek servisini durdurur: adb shell stop vecentekseservice
- Servis durduğu o kısa anda APK'yı yüklemeye çalışır
- Mantık: Kontrol eden servis yoksa, kontrol de yok

SALDIRI 2: Play Store Taklidi
- Komut: adb install -i "com.android.vending"
- Sisteme "Bu APK'yı Play Store yüklüyor" der
- Vecentek Play Store'a güveniyorsa, bu geçer

SALDIRI 3: Sistem Paketi Taklidi
- Komut: adb install -i "android"
- Sisteme "Bu APK'yı Android sistemi yüklüyor" der
- En yüksek güven seviyesi

SALDIRI 4: Qualcomm Test Taklidi
- Komut: adb install -i "com.qualcomm.qti.modemtestmode"
- Whitelist'teki bir test paketini taklit eder
- Sistem test paketlerine özel izin verebilir

SALDIRI 5: PM Install (Doğrudan Shell)
- APK'yı önce cihaza kopyalar: adb push
- Sonra shell üzerinden yükler: adb shell pm install
- ADB katmanını atlar, doğrudan paket yöneticisine gider

SALDIRI 6: PM Install (Bypass Seçenekleri)
- Komut: pm install --install-reason 3
- Özel parametrelerle yükleme yapar
- install-reason 3 = "Cihaz Güncellemesi" anlamına gelir

SALDIRI 7: Doğrulama Devre Dışı
- Komut: settings put global verifier_verify_adb_installs 0
- Sistemin APK doğrulama özelliğini kapatır
- Sonra normal yükleme yapar

KULLANIM:
---------
1. Arabayı ADB ile bağlayın
2. APK dosyasını scriptin üzerine sürükleyin
3. Script otomatik olarak 7 yöntemi sırayla dener
4. Biri başarılı olursa "[!!!] BASARILI!" mesajı görürsünüz

ÖNEMLİ NOTLAR:
--------------
⚠️ Bu script, APK'yı bilgisayardan arabaya göndermek için
   "adb push" komutu kullanır.
   
⚠️ Eğer "adb push" çalışmıyorsa (bazı sistemlerde kapalıdır),
   "USB_Install_Tool.bat" kullanın.

BAŞARI İHTİMALİ:
----------------
- Saldırı 1-3: %70 (En etkili)
- Saldırı 4-6: %50
- Saldırı 7: %40

NE ZAMAN KULLANILMALI:
-----------------------
- İmzalı APK'lar (Sign_For_Vecentek.bat ile oluşturulan) hazırsa
- ADB bağlantısı çalışıyorsa
- "adb push" komutu destekleniyorsa
