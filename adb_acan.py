@echo off
setlocal EnableDelayedExpansion

:: --- CONFIGURATION ---
set "TOOLS_DIR=D:\Home\BatchApkTool\bin"
set "OUTPUT_DIR=%~dp0"
set "APKTOOL=%TOOLS_DIR%\apktool_2.10.0_20240226.jar"
:: ---------------------

echo ========================================================
echo      ACTIVITY HUNTER (FIND INSTALL SCREENS)
echo ========================================================
echo.

if "%~1"=="" (
    echo [!] Lutfen APK dosyasini surukleyin!
    pause
    exit /b
)

set "INPUT_APK=%~1"
set "TEMP_DIR=%OUTPUT_DIR%\temp_activity_scan"

if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

echo [1/2] APK cozuluyor (Decompile)...
java -jar "%APKTOOL%" d -f -o "%TEMP_DIR%" "%INPUT_APK%" >nul

if not exist "%TEMP_DIR%\AndroidManifest.xml" (
    echo [!] Decompile hatasi!
    pause
    exit /b
)

echo.
echo [2/2] Aktiviteler Analiz Ediliyor...
echo --------------------------------------------------------
echo PAKET ISMI:
powershell -Command "$xml = [xml](Get-Content '%TEMP_DIR%\AndroidManifest.xml'); Write-Host $xml.manifest.package"
echo --------------------------------------------------------
echo.
echo BULUNAN "INSTALL" AKTIVITELERI:
echo (Bunlari 'adb shell am start -n ...' ile baslatabiliriz)
echo.

:: PowerShell ile XML analizi ve filtreleme
powershell -Command "$xml = [xml](Get-Content '%TEMP_DIR%\AndroidManifest.xml'); $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable); $ns.AddNamespace('android', 'http://schemas.android.com/apk/res/android'); $activities = $xml.SelectNodes('//activity', $ns); foreach ($a in $activities) { $name = $a.GetAttribute('name', 'http://schemas.android.com/apk/res/android'); if ($name -match 'Install' -or $name -match 'Package' -or $name -match 'Update' -or $name -match 'Download') { Write-Host '[+] POTANSIYEL HEDEF:' $name; $exported = $a.GetAttribute('exported', 'http://schemas.android.com/apk/res/android'); Write-Host '    Exported:' $exported; $filters = $a.SelectNodes('intent-filter', $ns); if ($filters.Count -gt 0) { Write-Host '    (Intent Filter var - Tetiklenebilir!)' } } }"

echo.
echo --------------------------------------------------------
echo TUM AKTIVITELER (Liste):
powershell -Command "$xml = [xml](Get-Content '%TEMP_DIR%\AndroidManifest.xml'); $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable); $activities = $xml.SelectNodes('//activity', $ns); foreach ($a in $activities) { Write-Host $a.GetAttribute('name', 'http://schemas.android.com/apk/res/android') }"
echo --------------------------------------------------------

:: Cleanup
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
pause
