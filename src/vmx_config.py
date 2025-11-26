import random
from pathlib import Path

from .vmx_utils import set_vmx_value, read_vmx, delete_vmx_value

OPTIMIZE_SETTINGS = {
    # Performance
    "prefvmx.minVmMemPct": "100",                       # 仮想マシンに割り当てる最小メモリを100%に設定
    "prefvmx.useRecommendedLockedMemSize": "TRUE",      # 推奨ロック済みメモリサイズを使用
    "priority.grabbed": "high",                         # アクティブ時のCPU優先度を高に設定
    "MemTrimRate": "0",                                 # メモリトリムレートを無効化


    # Security
    "isolation.tools.syncTime": "FALSE",                # ホストとの時刻同期を無効化
    "time.synchronize.continue": "FALSE",               # ゲストOSの継続時刻同期を無効化
    "time.synchronize.tools.enable": "FALSE",           # VMware Toolsによる時刻同期を無効化
    "tools.setInfo.sizeLimit": "1",                     # VMware Toolsでの情報送信サイズを最小に制限
    "tools.setInfo.disable": "TRUE",                    # VMware Toolsによる情報送信を無効化
    "printers.enabled": "FALSE",                        # ゲストOSからホストプリンタへのアクセスを無効化

    "sched.mem.pshare.enable": "FALSE",                 # メモリ共有を無効化
    "mainMem.useNamedFile": "FALSE",                    # メインメモリをファイルとして保存しない
    "mainMem.partialLazySave": "FALSE",                 # メモリを部分的に遅延保存しない
    "mainMem.partialLazyRestore": "FALSE",              # メモリを部分的に遅延復元しない
    "mainMem.useAnonymousMemory": "TRUE",               # メモリを匿名メモリとして確保し、.vmemファイルを作らない

    "logging": "FALSE",                                 # ログ出力を無効化
    "log.keepOld": "0",                                 # 古いログを保持しない
    "log.rotateSize": "0",                              # ログローテーションを無効化
    "debug": "FALSE",                                   # デバッグを無効化
}

ISOLATION_SETTINGS = {
    "isolation.tools.hgfs.disable": "TRUE",             # ホスト-ゲスト間の共有フォルダを無効化
    "isolation.tools.copy.disable": "TRUE",             # ゲストからホストへのコピーを無効化
    "isolation.tools.paste.disable": "TRUE",            # ホストからゲストへのペーストを無効化
    "isolation.tools.dnd.disable": "TRUE",              # ドラッグ&ドロップ操作を無効化
    "isolation.tools.setGUIOptions.enable": "FALSE"     # GUI設定変更機能を無効化
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


