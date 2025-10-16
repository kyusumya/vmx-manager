from pathlib import Path

from .vmx_config import is_config_applied

def scan_vmx_folder_for_status(vmx_folder: Path) -> dict[Path, dict]:
    """指定フォルダ内のVMXの最適化・スプーフィング状態を取得"""
    status = {}
    vmx_list = get_recent_vmx_from_folder(vmx_folder)
    for vmx in vmx_list:
        status[vmx] = {
            "optimized": is_config_applied(vmx, "optimize"),
            "spoofed": is_config_applied(vmx, "spoofing")
        }
    return status

def get_recent_vmx_from_preferences() -> list[Path]:
    """preferences.iniから最近開いたVMXを取得（存在するファイルのみ）"""
    ini_path = Path.home() / "AppData" / "Roaming" / "VMware" / "preferences.ini"
    vmx_files = []

    if not ini_path.exists():
        print(f"⚠️ preferences.ini が存在しません: {ini_path}")
        return vmx_files

    try:
        with open(ini_path, "r", encoding="cp932") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", ";")):
                    continue
                if "pref.ws.session.window" in line and ".file" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        path_str = parts[1].strip().strip('"')
                        if path_str:
                            path = Path(path_str)
                            if path.exists():
                                vmx_files.append(path)
    except Exception as e:
        print(f"⚠️ 読み込みエラー: {e}")

    return vmx_files

def get_recent_vmx_from_folder(vmx_folder: Path) -> list[Path]:
    """指定フォルダ以下のVMXファイルを取得"""
    if not vmx_folder or not vmx_folder.exists():
        print(f"⚠️ フォルダが存在しません: {vmx_folder}")
        return []
    return list(vmx_folder.rglob("*.vmx"))
