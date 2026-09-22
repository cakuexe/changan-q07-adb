@echo off
setlocal EnableDelayedExpansion

:: --- CONFIGURATION ---
set "TOOLS_DIR=D:\Home\BatchApkTool\bin"
set "OUTPUT_DIR=%~dp0"
set "APKTOOL=%TOOLS_DIR%\apktool_2.10.0_20240226.jar"
set "APKSIGNER=%TOOLS_DIR%\apksigner.jar"
set "PLATFORM_KEY=%TOOLS_DIR%\platform.pk8"
set "PLATFORM_CERT=%TOOLS_DIR%\platform.x509.pem"
:: ---------------------

echo ========================================================
echo      MARKET APP MODIFIER (TROJAN HORSE)
echo ========================================================
echo.

if "%~1"=="" (
    echo [!] Lutfen Market APK dosyasini (base.apk) surukleyin!
    pause
    exit /b
)

set "INPUT_APK=%~1"
set "FILENAME=%~n1"
set "TEMP_DIR=%OUTPUT_DIR%\temp_market_mod"

if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

echo [1/4] Market APK cozuluyor (Decompile)...
java -jar "%APKTOOL%" d -f -o "%TEMP_DIR%" "%INPUT_APK%"

if not exist "%TEMP_DIR%\AndroidManifest.xml" (
    echo [!] Decompile hatasi!
    pause
    exit /b
)

:: Find Package Name
echo.
echo [INFO] Paket Ismi Tespit Ediliyor...
powershell -Command "$xml = [xml](Get-Content '%TEMP_DIR%\AndroidManifest.xml'); Write-Host 'PACKAGE NAME: ' $xml.manifest.package"
echo.

echo [2/4] Debuggable Flag Ekleniyor...
powershell -Command "(Get-Content '%TEMP_DIR%\AndroidManifest.xml') -replace '<application', '<application android:debuggable=\"true\"' | Set-Content '%TEMP_DIR%\AndroidManifest.xml'"

echo [3/4] Tekrar Paketleniyor (Recompile)...
java -jar "%APKTOOL%" b -o "%TEMP_DIR%\dist\modded.apk" "%TEMP_DIR%"

if not exist "%TEMP_DIR%\dist\modded.apk" (
    echo [!] Paketleme hatasi!
    pause
    exit /b
)

echo [4/4] Imzalaniyor (Platform Key)...
java -jar "%APKSIGNER%" sign --key "%PLATFORM_KEY%" --cert "%PLATFORM_CERT%" --out "%OUTPUT_DIR%\market_modded_signed.apk" "%TEMP_DIR%\dist\modded.apk"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] BASARILI!
    echo Dosya: %OUTPUT_DIR%\market_modded_signed.apk
    echo.
    echo SIMDI YAPMANIZ GEREKENLER:
    echo 1. adb install -r market_modded_signed.apk
    echo 2. Eger yuklenirse, su komutu calistirin:
    echo    adb shell run-as <PAKET_ISMI> pm install /sdcard/waze.apk
) else (
    echo [!] Imzalama hatasi!
)

:: Cleanup
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
pause
