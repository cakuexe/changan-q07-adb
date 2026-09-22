import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import string
import subprocess
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class ADBManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Manager - Changan QiYuan Q07 1.2.0 VER")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # Tema və rənglər
        self.bg_color = "#1a1f3a"
        self.card_color = "#252b4a"
        self.accent_color = "#e63946"
        self.text_color = "#e4e7eb"
        self.secondary_text = "#9ca3af"
        self.root.configure(bg=self.bg_color)

        # Kod və API URL
        self.current_code = ""
        self.api_url = "https://cakudashboard.xo.je/api/changan/qiyuan/120/l31irsjr7At4OAdbtcRkjwtBfdn4mtgP.php"

        # Custom APK qovluğu
        self.custom_apks_folder = Path("custom_apks")
        self.custom_apks_folder.mkdir(exist_ok=True)

        self.create_widgets()
        self.generate_new_code()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20, padx=20, fill="x")
        tk.Label(header_frame, text="🚗 ADB Manager", font=("Segoe UI", 24, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack()
        tk.Label(header_frame, text="Changan Qiyuan 120 - Sistem İdarəetməsi", font=("Segoe UI", 10),
                 bg=self.bg_color, fg=self.secondary_text).pack()

        # Kod Frame
        code_frame = tk.Frame(self.root, bg=self.card_color, relief="raised", bd=2)
        code_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(code_frame, text="Aktivasiya Kodu:", font=("Segoe UI", 11, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(pady=(15,5))

        self.code_entry = tk.Entry(code_frame, font=("Consolas", 12), width=40, justify="center",
                                   state="readonly", readonlybackground=self.bg_color,
                                   fg=self.accent_color, bd=0, relief="flat")
        self.code_entry.pack(pady=5)

        self.verify_button = tk.Button(code_frame, text="🔍 Kodu Yoxla", font=("Segoe UI", 11, "bold"),
                                       bg=self.accent_color, fg="white", activebackground="#d62828",
                                       activeforeground="white", bd=0, padx=30, pady=10,
                                       cursor="hand2", command=self.verify_code)
        self.verify_button.pack(pady=15)

        self.status_label = tk.Label(code_frame, text="", font=("Segoe UI",10),
                                     bg=self.card_color, fg=self.secondary_text)
        self.status_label.pack(pady=(0,10))

        # ADB Commands
        commands_frame = tk.LabelFrame(self.root, text="ADB Əmrləri", font=("Segoe UI", 11, "bold"),
                                       bg=self.card_color, fg=self.text_color, bd=2, relief="raised")
        commands_frame.pack(pady=10, padx=20, fill="x")

        buttons_data = [
            ("🔓 ADB Aç", self.open_adb, "#10b981"),
            ("🔒 ADB Bağla", self.close_adb, "#ef4444"),
            ("🛡️ Qoruma Sistemini Bağla", self.disable_protection, "#f59e0b"),
            ("📦 Custom APK Yüklə", self.install_custom_apks, "#6366f1")
        ]

        for i, (text, cmd, color) in enumerate(buttons_data):
            row, col = i//2, i%2
            btn = tk.Button(commands_frame, text=text, font=("Segoe UI",10,"bold"),
                            bg=color, fg="white", activebackground=color, activeforeground="white",
                            bd=0, padx=15, pady=12, cursor="hand2", command=cmd, state="disabled")
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            commands_frame.columnconfigure(col, weight=1)
            if i==0: self.btn_open_adb=btn
            elif i==1: self.btn_close_adb=btn
            elif i==2: self.btn_disable_protection=btn
            elif i==3: self.btn_install_apks=btn

        # Log Bölməsi
        log_frame = tk.LabelFrame(self.root, text="Log / Çıxış", font=("Segoe UI", 11, "bold"),
                                  bg=self.card_color, fg=self.text_color, bd=2, relief="raised")
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_text = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9),
                                                  bg=self.bg_color, fg=self.text_color,
                                                  insertbackground=self.text_color,
                                                  wrap="word", height=10, bd=0, relief="flat")
        self.log_text.pack(padx=10, pady=10, fill="both", expand=True)

        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(footer_frame, text="© 2024 ADB Manager Tool", font=("Segoe UI", 8),
                 bg=self.bg_color, fg=self.secondary_text).pack()

    def generate_new_code(self):
        characters = string.ascii_letters + string.digits
        self.current_code = ''.join(random.choice(characters) for _ in range(32))
        self.code_entry.config(state="normal")
        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, self.current_code)
        self.code_entry.config(state="readonly")
        self.log(f"🔑 Yeni kod generasiya edildi: {self.current_code}")

    def verify_code(self):
        self.verify_button.config(state="disabled", text="⏳ Yoxlanılır...")
        self.status_label.config(text="Kod yoxlanılır...", fg="#f59e0b")

        def thread_verify():
            try:
                result = self.check_code_selenium(self.current_code)
                if result:
                    self.root.after(0, self.on_verification_success)
                else:
                    self.root.after(0, self.on_verification_failed)
            except Exception as e:
                self.root.after(0, lambda: self.log(f"❌ Xəta: {str(e)}"))
                self.root.after(0, self.on_verification_failed)

        threading.Thread(target=thread_verify, daemon=True).start()

    def check_code_selenium(self, code):
        url = f"{self.api_url}?code={code}"
        options = Options()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            self.log(f"📡 Selenium ilə URL açılır: {url}")
            driver.get(url)
            time.sleep(3)  # JS işləməsi üçün
            final_url = driver.current_url
            self.log(f"📥 Son URL: {final_url}")
            # Sadə yoxlama: yönləndirilmiş URL parametri ilə təsdiqlə
            if "i=1" in final_url:
                self.log("✅ Kod aktivdir (Selenium vasitəsilə)")
                return True
            else:
                self.log("❌ Kod aktiv deyil (Selenium vasitəsilə)")
                return False
        finally:
            driver.quit()

    # ADB əmrləri eyni qalır
    def run_adb_command(self, commands, description):
        def run_thread():
            self.log(f"⚙️ {description} başladı...")
            try:
                if isinstance(commands, str):
                    commands = [commands]
                for cmd in commands:
                    self.log(f"🔧 Əmr: {cmd}")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                    if result.stdout:
                        self.root.after(0, lambda out=result.stdout: self.log(f"📤 {out.strip()}"))
                    if result.stderr:
                        self.root.after(0, lambda err=result.stderr: self.log(f"⚠️ {err.strip()}"))
                    if result.returncode == 0:
                        self.root.after(0, lambda: self.log("✅ Əmr uğurla icra edildi"))
                    else:
                        self.root.after(0, lambda: self.log(f"❌ Əmr xətası: Kod {result.returncode}"))
                self.root.after(0, lambda: self.log(f"✅ {description} tamamlandı!\n"))
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: self.log(f"❌ Timeout: Əmr çox uzun çəkdi\n"))
            except Exception as e:
                self.root.after(0, lambda err=str(e): self.log(f"❌ Xəta: {err}\n"))

        threading.Thread(target=run_thread, daemon=True).start()

    def open_adb(self):
        self.run_adb_command([
            "adb wait-for-device",
            "adb shell setprop a.adb.1 1",
            "adb shell setprop vecentek_adb_verification 0",
            "adb shell setprop adb_install 1",
            "adb shell setprop persist.usb.prim.adb_switch on"
        ], "ADB Açma")

    def close_adb(self):
        self.run_adb_command([
            "adb wait-for-device",
            "adb shell setprop persist.usb.prim.adb_switch off"
        ], "ADB Bağlama")

    def disable_protection(self):
        self.run_adb_command("adb shell setprop vecentek.model 1", "Qoruma Sistemini Bağlama")

    def install_custom_apks(self):
        apk_files = list(self.custom_apks_folder.glob("*.apk"))
        if not apk_files:
            messagebox.showwarning("APK Tapılmadı",
                                   f"'{self.custom_apks_folder}' qovluğunda APK faylı tapılmadı.")
            self.log(f"⚠️ '{self.custom_apks_folder}' qovluğunda APK tapılmadı")
            return

        self.log(f"📦 {len(apk_files)} APK faylı tapıldı")
        def install_thread():
            for apk_file in apk_files:
                apk_name = apk_file.name
                remote_path = f"/data/local/tmp/{apk_name}"
                self.root.after(0, lambda name=apk_name: self.log(f"\n📱 {name} yüklənir..."))
                try:
                    push_cmd = f'adb push "{apk_file}" {remote_path}'
                    self.root.after(0, lambda: self.log(f"🔧 Push: {push_cmd}"))
                    result = subprocess.run(push_cmd, shell=True, capture_output=True, text=True, timeout=60)
                    if result.returncode != 0:
                        self.root.after(0, lambda err=result.stderr: self.log(f"❌ Push xətası: {err}"))
                        continue
                    self.root.after(0, lambda: self.log(f"✅ Push uğurlu"))
                    install_cmd = f"adb install -g {remote_path}"
                    self.root.after(0, lambda: self.log(f"🔧 Install: {install_cmd}"))
                    result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True, timeout=60)
                    if "Success" in result.stdout:
                        self.root.after(0, lambda name=apk_name: self.log(f"✅ {name} uğurla quruldu"))
                    else:
                        self.root.after(0, lambda out=result.stdout: self.log(f"❌ Qurulum xətası: {out}"))
                except subprocess.TimeoutExpired:
                    self.root.after(0, lambda: self.log(f"❌ Timeout: Əməliyyat çox uzun çəkdi"))
                except Exception as e:
                    self.root.after(0, lambda err=str(e): self.log(f"❌ Xəta: {err}"))
            self.root.after(0, lambda: self.log(f"\n✅ Bütün APK əməliyyatları tamamlandı!"))

        threading.Thread(target=install_thread, daemon=True).start()

    def on_verification_success(self):
        self.log("✅ Kod təsdiqləndi! Sistem aktivləşdirildi.")
        self.status_label.config(text="✅ Aktivasiya uğurlu!", fg="#10b981")
        self.verify_button.config(state="disabled", text="✅ Aktivləşdirildi")
        self.btn_open_adb.config(state="normal")
        self.btn_close_adb.config(state="normal")
        self.btn_disable_protection.config(state="normal")
        self.btn_install_apks.config(state="normal")
        messagebox.showinfo("Uğurlu", "Sistem aktivləşdirildi! İndi ADB əmrlərini istifadə edə bilərsiniz.")

    def on_verification_failed(self):
        self.log("❌ Kod təsdiqlənmədi. Yeni kod generasiya edilir...")
        self.status_label.config(text="❌ Kod yanlışdır", fg="#ef4444")
        self.verify_button.config(state="normal", text="🔍 Kodu Yoxla")
        self.generate_new_code()

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.update()

def main():
    root = tk.Tk()
    app = ADBManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
