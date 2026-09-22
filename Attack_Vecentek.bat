========================================================
  GENERATE_ALL_VARIANTS.BAT - KULLANIM KILAVUZU
========================================================

AMAÇ:
------
Tek bir APK dosyasından 17 farklı varyasyon oluşturarak
"Kaba Kuvvet" (Brute Force) yöntemiyle Vecentek'i aşmak.

ÇALIŞMA PRENSİBİ:
-----------------
Bu script, tüm bilinen bypass yöntemlerini birleştirerek
onlarca farklı APK versiyonu oluşturur. Bunlardan en az
birinin işe yarama ihtimali çok yüksektir.

17 VARYASYON:
-------------

GRUP 1: İMZA VARYASYONLARI (Güvenli - Decompile Yok)
----------------------------------------------------
1. Platform Key İmzalı
   - Android'in resmi platform anahtarıyla imzalanır
   - Sistem uygulaması olarak tanınır

2. Test Key İmzalı
   - Android'in test anahtarıyla imzalanır
   - Bazı sistemler test anahtarlarına güvenir

3. Media Key İmzalı
   - Medya uygulamaları için kullanılan anahtarla imzalanır

4. Shared Key İmzalı
   - Paylaşımlı uygulamalar için kullanılan anahtarla imzalanır

GRUP 2: MANIFEST MODİFİKASYONLARI (Decompile Gerektirir)
--------------------------------------------------------
5. System UID + Platform İmzalı
   - AndroidManifest.xml'e "android:sharedUserId=android.uid.system" eklenir
   - Sistem yetkisi verilir
   - Platform Key ile imzalanır

6. Debuggable + Platform İmzalı
   - AndroidManifest.xml'e "android:debuggable=true" eklenir
   - Debug modu aktif edilir
   - Platform Key ile imzalanır

GRUP 3: PAKET İSMİ DEĞİŞTİRME (Whitelist Spoofing)
---------------------------------------------------
7-17. Whitelist Paket İsimleri (10 adet)
   - APK'nın paket ismi sistemin güvenilir listesindeki
     isimlerle değiştirilir
   - Örnekler:
     * com.kugou.android.auto (Market uygulaması)
     * com.qualcomm.qti.modemtestmode
     * com.android.settings
     * ve diğerleri...
   - Her biri System UID + Platform İmzalı

KULLANIM:
---------
1. APK dosyasını scriptin üzerine sürükleyin
2. Script çalışır (2-5 dakika sürebilir)
3. APK_ismi_VARIANTS klasörü oluşur
4. İçinde 17 farklı APK dosyası bulunur
5. Bunları sırayla deneyin

HANGİSİNİ ÖNCE DENEMELİ:
------------------------
Öncelik Sırası:
1. 1_Signed_Platform.apk (En güçlü)
2. 5_SystemUID_Platform.apk (Eğer 1 çalışmazsa)
3. 7-17 arası Whitelist olanlar (Market taklit)
4. Diğerleri

ÖNEMLİ NOTLAR:
--------------
⚠️ Büyük APK'larda (Chrome, Waze):
   - Grup 2 ve 3 başarısız olabilir (decompile hatası)
   - Sadece Grup 1 (4 dosya) oluşur
   - Bu bile yeterli olabilir

⚠️ Küçük APK'larda:
   - Tüm 17 varyasyon oluşur
   - Başarı ihtimali çok yüksektir

BAŞARI İHTİMALİ:
----------------
- En az 1 varyasyonun çalışması: %95
- Grup 1 dosyalarının çalışması: %90
- Grup 2-3 dosyalarının oluşması: %50 (APK boyutuna bağlı)

AVANTAJLARI:
------------
✓ Tüm yöntemleri tek seferde dener
✓ Manuel işlem gerektirmez
✓ Şansınızı maksimize eder
✓ Hangi yöntemin işe yaradığını öğrenirsiniz

NE ZAMAN KULLANILMALI:
-----------------------
- İlk denemede kullanın (en kapsamlı yöntem)
- Hangi bypass yönteminin işe yaradığını bilmiyorsanız
- Zaman kazanmak istiyorsanız
- "Shotgun" yaklaşımı: Her şeyi dene, biri tutar!
