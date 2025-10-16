import platform

from src.ui import main_menu

def main():
    """エントリーポイント"""
    if platform.system() == "Windows":
        main_menu()
    else:
        print("現在、Windows以外のOSはサポートしていません")

if __name__ == "__main__":
    main()