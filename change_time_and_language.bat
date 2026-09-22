adb shell am start -a androids.settings.SETTINGS

:: Set timezone
adb shell setprop persist.sys.timezone "Asia/Baku"

:: Set language and region to US English
adb shell "settings put system system_locales en-US"
adb shell "setprop persist.sys.locale en-US"

:: Restart system UI to apply immediately (without full reboot)
adb shell "am restart"