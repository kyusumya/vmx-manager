import locale
from typing import Optional

# サポート言語
LANGUAGES = ["ja", "en"]

# 翻訳辞書
TRANSLATIONS = {
    "ja": {
        "menu_optimize": "VM最適化",
        "menu_spoofing": "VMスプーフィング",
        "menu_isolation": "VM統合機能",
        "menu_status": "設定状況確認",
        "menu_settings": "設定",
        "menu_exit": "閉じる",
        "menu_select": "メニューを選択してください",
        "menu_language": "言語設定",
        "menu_vmx_folder": "VMXフォルダー設定",
        "menu_back": "戻る",
        "prompt_language": "言語を入力してください (例: ja, en):",
        "prompt_vmx_folder": "VMX取得フォルダーを選択してください",
        "select_vmx": "VMXを選択してください",
        "folder_not_exist": "⚠️ フォルダが存在しません",
        "file_not_exist": "⚠️ VMXファイルは見つかりませんでした",
        "optimized": "最適化",
        "spoofed": "スプーフィング",
        "done": "設定済み",
        "fail": "書き込み失敗",
        "press_any_key": "任意のキーを押して戻る…",
        "instruction_checkbox": "スペースで選択、Enterで確定",
        "vmx_source": "📂 VMX取得方法"
    },
    "en": {
        "menu_optimize": "Optimize VM",
        "menu_spoofing": "VM Spoofing",
        "menu_isolation": "VM Isolation",
        "menu_status": "Check Status",
        "menu_settings": "Settings",
        "menu_exit": "Exit",
        "menu_select": "Select menu",
        "menu_language": "Language",
        "menu_vmx_folder": "VMX Folder",
        "menu_back": "Back",
        "prompt_language": "Enter language (e.g., ja, en):",
        "prompt_vmx_folder": "Select VMX folder",
        "select_vmx": "Select VMX",
        "folder_not_exist": "⚠️ Folder does not exist",
        "file_not_exist": "⚠️ No VMX file found",
        "optimized": "Optimized",
        "spoofed": "Spoofed",
        "done": "Done",
        "fail": "Write failed",
        "press_any_key": "Press any key to return...",
        "instruction_checkbox": "Space to select, Enter to confirm",
        "vmx_source": "📂 VMX Source"
    }
}

def get_system_language() -> str:
    """システムの言語コードを取得"""
    lang, _ = locale.getdefaultlocale()
    if not lang:
        return "en"
    lang_code = lang.split("_")[0]
    return lang_code if lang_code in LANGUAGES else "en"

def t(key: str, settings: Optional[dict] = None) -> str:
    """翻訳文字列を取得"""
    lang = settings.get("language") if settings else None
    if not lang:
        lang = get_system_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
