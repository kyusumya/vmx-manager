import re
from pathlib import Path
from typing import Optional

from .vmx_config import is_config_applied
from .lang import t

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

def get_recent_vmx_from_inventory(settings: Optional[dict] = None, vmx_folder: Path = None) -> list[Path]:
    """
    inventory.vmls から VMX パスを取得
    index*.id = "フルパス" の形式を読み取る
    """
    vmx_files = []

    inventory_path = Path.home() / "AppData" / "Roaming" / "VMware" / "inventory.vmls"

    if not inventory_path.exists():
        print(t("file_not_exist", settings))
        return vmx_files

    pattern = re.compile(r'index\d+\.id\s*=\s*"(.+\.vmx)"', re.IGNORECASE)

    try:
        with open(inventory_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", ";")):
                    continue
                match = pattern.match(line)
                if match:
                    path_str = match.group(1)
                    path = Path(path_str)
                    if path.exists():
                        vmx_files.append(path)
    except Exception as e:
        print(f"⚠️ {t('fail', settings)}: {e}")

    return vmx_files

def get_recent_vmx_from_folder(vmx_folder: Path, settings: Optional[dict] = None) -> list[Path]:
    """指定フォルダ以下のVMXファイルを取得"""
    if not vmx_folder or not vmx_folder.exists():
        print(t("folder_not_exist", settings))
        return []
    return list(vmx_folder.rglob("*.vmx"))