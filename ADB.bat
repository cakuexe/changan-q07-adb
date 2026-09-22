========================================================
  RENAME_TO_WHITELIST.BAT - KULLANIM KILAVUZU
========================================================

AMAÇ:
------
APK'nın paket ismini sistemin "güvenilir" listesindeki (whitelist)
bir paket ismiyle değiştirerek Vecentek'i kandırmak.

ÇALIŞMA PRENSİBİ:
-----------------
1. Hedef Paket İsmi: com.kugou.android.auto
   - Bu, arabanın Market uygulamasının paket ismidir
   - Sistem bu isme güvenir ve Vecentek kontrolü yapmaz

2. İşlem Adımları:
   a) APK'yı decompile eder (apktool ile açar)
   b) AndroidManifest.xml dosyasını bulur
   c) package="com.waze" gibi satırı bulur
   d) Bunu package="com.kugou.android.auto" olarak değiştirir
   e) Ayrıca "android:sharedUserId=android.uid.system" ekler
   f) APK'yı tekrar paketler (recompile)
   g) Platform Key ile imzalar

3. Sonuç:
   - Sistem bu APK'yı "Market Uygulaması Güncellemesi" sanar
   - Vecentek kontrolü atlanır
   - ÇIKTI: filename_renamed_whitelisted.apk

KULLANIM:
---------
1. APK dosyasını scriptin üzerine sürükleyin
2. Script işlemi yapar (1-2 dakika sürebilir)
3. Oluşan dosyayı yükleyin

ÖNEMLİ UYARILAR:
----------------
⚠️ Paket ismi değiştiği için:
   - Uygulama Google servisleriyle bağlantı kuramayabilir
   - Login/Harita özellikleri çalışmayabilir
   - Ancak uygulama açılır ve temel işlevler çalışır

⚠️ Büyük APK'larda (Chrome, Waze):
   - Decompile/Recompile başarısız olabilir
   - Kaynak dosyalarında (resources) hata çıkabilir
   - Bu durumda "Sign_For_Vecentek.bat" kullanın

BAŞARI İHTİMALİ:
----------------
- Küçük APK'lar: %85
- Büyük APK'lar: %40 (teknik zorluklar nedeniyle)

NE ZAMAN KULLANILMALI:
-----------------------
- "Sign_For_Vecentek.bat" çalışmadıysa
- Sistem sadece belirli paket isimlerine izin veriyorsa
- Son çare olarak
