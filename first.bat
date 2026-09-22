========================================================
  USB_INSTALL_TOOL.BAT - KULLANIM KILAVUZU
========================================================

AMAÇ:
------
"adb push" çalışmayan sistemlerde, USB bellekteki APK'ları
doğrudan arabadan yüklemek.

ÇALIŞMA PRENSİBİ:
-----------------
1. APK'lar USB belleğe kopyalanır
2. USB bellek arabaya takılır
3. Script, ADB üzerinden arabaya komut gönderir
4. Araba, kendi USB'sindeki dosyayı yükler
5. Dosya transferi olmadığı için "adb push" gerekmez

KULLANIM ADIMLARI:
------------------

ADIM 1: USB Hazırlama
- İmzalanmış APK'ları USB belleğe kopyalayın
- Örnek: chrome_signed_platform.apk

ADIM 2: USB'yi Arabaya Takma
- USB belleği arabanın USB portuna takın
- Sistem otomatik olarak tanımalı

ADIM 3: Script Çalıştırma
- Bilgisayardan "USB_Install_Tool.bat" dosyasını çalıştırın
- Script size USB yolunu soracak

ADIM 4: USB Yolunu Bulma
- Script otomatik olarak depolama alanlarını listeler
- Genelde şu yollardan biri olur:
  * /storage/sda1
  * /storage/udisk
  * /storage/usb0
  * /mnt/usb_storage
- Listeden tahmin edin ve yazın

ADIM 5: Dosya İsmini Girme
- USB'deki APK dosyasının tam ismini yazın
- Örnek: chrome_signed_platform.apk

ADIM 6: Otomatik Deneme
Script 5 farklı yöntemi dener:
1. Normal pm install
2. Play Store taklidi (-i vending)
3. Sistem taklidi (-i android)
4. Whitelist taklidi (-i qualcomm)
5. Servis durdurma + yükleme

ÖRNEK KULLANIM:
---------------
> USB Bellegin Yolu: /storage/sda1
> Dosya Ismi: chrome_signed_platform.apk

Script şu komutu çalıştırır:
adb shell pm install -r /storage/sda1/chrome_signed_platform.apk

USB YOLUNU BULAMIYOR MUSUNUZ?
------------------------------
Şu komutu manuel çalıştırın:
adb shell ls -d /storage/* /mnt/*

Çıktıda "sda1", "udisk", "usb" gibi kelimeler arayın.

BAŞARI İHTİMALİ:
----------------
- %85 (adb push gerektirmediği için çok güvenilir)

AVANTAJLARI:
------------
✓ "adb push" çalışmasa bile işe yarar
✓ Büyük dosyalar için hızlıdır
✓ Birden fazla APK deneyebilirsiniz

NE ZAMAN KULLANILMALI:
-----------------------
- "Attack_Vecentek.bat" "adb push" hatası veriyorsa
- Sistem dosya transferini engelliyorsa
- Birden fazla APK denemek istiyorsanız
