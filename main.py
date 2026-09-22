@echo off
chcp 65001 >nul
title ADB автоактивация при подключении
echo ===============================================
echo Ожидание устройства...
adb wait-for-device
echo Устройство обнаружено! Выполняются команды...
echo ===============================================

adb shell setprop a.adb.1 1
adb shell setprop vecentek_adb_verification 0
adb shell setprop adb_install 1
adb shell setprop persist.usb.prim.adb_switch on

echo ===============================================
echo Команды выполнены!
echo Теперь ты можешь вводить свои команды вручную.
echo ===============================================
cmd /k
