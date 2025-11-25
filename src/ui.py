import os
import platform
import sys
from pathlib import Path
from InquirerPy import inquirer
import tkinter as tk
from tkinter import filedialog

from .vmx_config import apply_config, is_config_applied
from .vmx_list import get_recent_vmx_from_inventory, get_recent_vmx_from_folder
from .lang import t

# クロスプラットフォーム任意キー待ち
if platform.system() == "Windows":
    import msvcrt
    def wait_key(prompt="Press any key to return..."):
        print(prompt, end="", flush=True)
        msvcrt.getch()
        print()
else:
    import tty, termios
    def wait_key(prompt="Press any key to return..."):
        print(prompt, end="", flush=True)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print()

def clear_screen():
    """画面クリア"""
    os.system("cls" if platform.system() == "Windows" else "clear")

def select_vmx_folder(settings: dict, default_path=None) -> Path | None:
    """フォルダ選択ダイアログ"""
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(
        initialdir=default_path or str(Path.home()),
        title=t("prompt_vmx_folder", settings)
    )
    return Path(folder) if folder else None

def select_vmx_list(settings: dict, message_key="select_vmx", vmx_folder: Path = None) -> list[Path]:
    """VMXリスト選択（CLI）"""
    vmx_list = get_recent_vmx_from_folder(vmx_folder) if vmx_folder else get_recent_vmx_from_inventory()
    vmx_list = [p for p in vmx_list if p.exists()]

    if not vmx_list:
        print(t("file_not_exist", settings))
        return []

    choices = [{"name": str(p), "value": p} for p in vmx_list]
    selected = inquirer.checkbox(
        message=t(message_key, settings),
        choices=choices,
        instruction=t("instruction_checkbox", settings)
    ).execute()
    return selected

def settings_menu(settings: dict):
    """設定メニュー"""
    while True:
        clear_screen()
        choice = inquirer.select(
            message=t("menu_settings", settings),
            choices=[
                {"name": t("menu_language", settings), "value": "language"},
                {"name": t("menu_vmx_folder", settings), "value": "vmx_folder"},
                {"name": t("menu_back", settings), "value": "back"}
            ],
        ).execute()

        if choice == "language":
            lang = inquirer.text(
                message=t("prompt_language", settings),
                default=settings.get("language", "ja")
            ).execute()
            settings["language"] = lang
            print(f"✅ {lang}")
            wait_key(t("press_any_key", settings))

        elif choice == "vmx_folder":
            folder = select_vmx_folder(settings, settings.get("vmx_folder"))
            if folder and folder.exists():
                settings["vmx_folder"] = folder
                print(f"✅ {folder}")
            else:
                print(t("folder_not_exist", settings))
            wait_key(t("press_any_key", settings))

        elif choice == "back":
            break

def main_menu():
    """メインメニュー"""
    settings = {}

    while True:
        clear_screen()
        vmx_source = f"{t('vmx_source', settings)}: {settings['vmx_folder']}" if settings.get("vmx_folder") else f"{t('vmx_source', settings)}: inventory.vmls"
        print(vmx_source + "\n")

        choice = inquirer.select(
            message=t("menu_select", settings),
            choices=[
                {"name": t("menu_optimize", settings), "value": "optimize"},
                {"name": t("menu_spoofing", settings), "value": "spoofing"},
                {"name": t("menu_isolation", settings), "value": "isolation"},
                {"name": t("menu_status", settings), "value": "status"},
                {"name": t("menu_settings", settings), "value": "settings"},
                {"name": t("menu_exit", settings), "value": "exit"}
            ],
        ).execute()

        if choice in ["optimize", "spoofing", "isolation"]:
            selected_vmx = select_vmx_list(settings, f"menu_{choice}", settings.get("vmx_folder"))
            if not selected_vmx:
                wait_key(t("press_any_key", settings))
                continue
            for vmx in selected_vmx:
                try:
                    apply_config(vmx, choice)
                    print(f"✅ {vmx} {t('done', settings)}")
                except Exception as e:
                    print(f"⚠️ {vmx} {t('fail', settings)}: {e}")
            wait_key(t("press_any_key", settings))

        elif choice == "status":
            clear_screen()
            vmx_list = get_recent_vmx_from_folder(settings.get("vmx_folder")) if settings.get("vmx_folder") else get_recent_vmx_from_inventory()
            vmx_list = [p for p in vmx_list if p.exists()]

            if not vmx_list:
                print(t("file_not_exist", settings))
            else:
                print("📋 " + t("menu_status", settings))
                for vmx in vmx_list:
                    spoofed = "✅" if is_config_applied(vmx, "spoofing") else "❌"
                    optimized = "✅" if is_config_applied(vmx, "optimize") else "❌"
                    isolation = "✅" if is_config_applied(vmx, "isolation") else "❌"
                    
                    print(f"{t('spoofed', settings)}: {spoofed} | {t('optimized', settings)}: {optimized} | {t('isolation', settings)}: {isolation} | {vmx}")
            wait_key(t("press_any_key", settings))

        elif choice == "settings":
            settings_menu(settings)

        elif choice == "exit":
            print("👋 " + t("menu_exit", settings))
            break
