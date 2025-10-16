from pathlib import Path

def read_vmx(vmx_path: Path) -> dict:
    """VMXファイルを辞書として読み込む"""
    if not vmx_path.exists():
        raise FileNotFoundError(f"{vmx_path} が存在しません。")
    vmx_data = {}
    with open(vmx_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", ";")):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            vmx_data[key.strip()] = value.strip().strip('"')
    return vmx_data

def write_vmx(vmx_path: Path, vmx_data: dict):
    """辞書形式のVMXデータを書き込む"""
    with open(vmx_path, "w", encoding="utf-8") as f:
        f.write("\n".join(f'{k} = "{v}"' for k, v in vmx_data.items()) + "\n")

def set_vmx_value(vmx_path: Path, key: str, value: str):
    """VMXに値を設定（上書きまたは追加）"""
    data = read_vmx(vmx_path)
    data[key] = value
    write_vmx(vmx_path, data)

def get_vmx_value(vmx_path: Path, key: str):
    """VMXから値を取得（存在しなければNone）"""
    return read_vmx(vmx_path).get(key)

def delete_vmx_value(vmx_path: Path, key: str):
    """VMXからキーを削除"""
    data = read_vmx(vmx_path)
    if key in data:
        del data[key]
        write_vmx(vmx_path, data)
