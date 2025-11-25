import random
from pathlib import Path

from .vmx_utils import set_vmx_value, read_vmx, delete_vmx_value

OPTIMIZE_SETTINGS = {
    "sched.mem.pshare.enable": "FALSE",            # メモリ共有を無効化
    "mainMem.useNamedFile": "FALSE",               # メインメモリをファイルとして保存しない
    "prefvmx.minVmMemPct": "100",                  # 仮想マシンに割り当てる最小メモリを100%に設定
    "prefvmx.useRecommendedLockedMemSize": "TRUE", # 推奨ロック済みメモリサイズを使用
    "mainMem.partialLazySave": "FALSE",            # メモリを部分的に遅延保存しない
    "mainMem.partialLazyRestore": "FALSE",         # メモリを部分的に遅延復元しない
    "priority.grabbed": "high",                    # アクティブ時のCPU優先度を高に設定
    "logging": "FALSE",                            # ログ出力を無効化
    "log.keepOld": "0",                            # 古いログを保持しない
    "log.rotateSize": "0",                         # ログローテーションを無効化
    "mainMem.useAnonymousMemory": "TRUE",          # メモリを匿名メモリとして確保し、.vmemファイルを作らない
    "MemTrimRate": "0",                            # メモリトリムレートを無効化
    "isolation.tools.syncTime": "FALSE"            # ホストとの時刻同期を無効化
}

ISOLATION_SETTINGS = {
    "isolation.tools.hgfs.disable": "TRUE",
    "isolation.tools.copy.disable": "TRUE",
    "isolation.tools.paste.disable": "TRUE",
    "isolation.tools.setGUIOptions.enable": "FALSE"
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

def apply_isolation(vmx_path: Path):
    """ホスト統合機能をトグル式で設定"""
    vmx_data = read_vmx(vmx_path)
    for k, v in ISOLATION_SETTINGS.items():
        if k in vmx_data:
            delete_vmx_value(vmx_path, k)
        else:
            set_vmx_value(vmx_path, k, v)

def apply_config(vmx_path: Path, group_name: str):
    """グループに応じてVMXに設定を適用"""
    if group_name == "optimize":
        apply_optimization(vmx_path)
    elif group_name == "spoofing":
        apply_spoofing(vmx_path)
    elif group_name == "isolation":
        apply_isolation(vmx_path)
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
        elif group_name == "isolation":
            return all(vmx_data.get(k) == v for k, v in ISOLATION_SETTINGS.items())
    except Exception:
        return False
    raise ValueError(f"設定グループが存在しません: {group_name}")

