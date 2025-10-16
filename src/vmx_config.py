import random
from pathlib import Path

from .vmx_utils import set_vmx_value, read_vmx

OPTIMIZE_SETTINGS = {
    "sched.mem.pshare.enable": "FALSE",
    "mainMem.useNamedFile": "FALSE",
    "prefvmx.minVmMemPct": "100",
    "prefvmx.useRecommendedLockedMemSize": "TRUE",
    "mainMem.partialLazySave": "FALSE",
    "mainMem.partialLazyRestore": "FALSE",
    "priority.grabbed": "high",
    "priority.ungrabbed": "normal",
}

def apply_optimization(vmx_path: Path):
    """VMXに最適化設定を書き込む"""
    for k, v in OPTIMIZE_SETTINGS.items():
        set_vmx_value(vmx_path, k, v)

def apply_spoofing(vmx_path: Path):
    """VMXにランダムUUIDを書き込む"""
    random_bytes = [random.randint(0, 255) for _ in range(16)]
    hex_bytes = [f"{b:02x}" for b in random_bytes]
    generated_uuid = ' '.join(hex_bytes[:8]) + '-' + ' '.join(hex_bytes[8:])
    set_vmx_value(vmx_path, "uuid.action", "keep")
    set_vmx_value(vmx_path, "uuid.bios", generated_uuid)
    set_vmx_value(vmx_path, "smbios.uuid", generated_uuid)

def apply_config(vmx_path: Path, group_name: str):
    """グループに応じてVMXに設定を適用"""
    if group_name == "optimize":
        apply_optimization(vmx_path)
    elif group_name == "spoofing":
        apply_spoofing(vmx_path)
    else:
        raise ValueError(f"設定グループが存在しません: {group_name}")

def is_config_applied(vmx_path: Path, group_name: str) -> bool:
    """設定がVMXに適用済みか確認"""
    try:
        vmx_data = read_vmx(vmx_path)
        if group_name == "spoofing":
            return "uuid.bios" in vmx_data and "smbios.uuid" in vmx_data
        elif group_name == "optimize":
            return all(vmx_data.get(k) == v for k, v in OPTIMIZE_SETTINGS.items())
    except Exception:
        return False
    raise ValueError(f"設定グループが存在しません: {group_name}")

