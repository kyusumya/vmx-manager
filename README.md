# ⚙️ VMX Manager

**VMware Workstation / Player** の `.vmx` 設定ファイルをCLI で簡単に最適化 & スプーフィングできるツールです 💻  

---

## 🚀 主な機能

| 機能 | 説明 |
|------|------|
| 🧠 **VM最適化 (Optimize VM)** | VMware のパフォーマンスを向上させるために、`mainMem` や `sched.mem` の設定を自動調整します。 |
| 🎭 **VMスプーフィング (VM Spoofing)** | ランダムな UUID を自動生成し、ホスト識別情報を偽装します。 |
| 📋 **設定状況確認 (Check Status)** | 各 VMX ファイルに最適化 / スプーフィング設定が適用されているか確認します。 |
| ⚙️ **設定メニュー (Settings)** | 言語設定（日本語 / 英語）や VMX フォルダを指定可能。 |
| 💾 **preferences.ini 読み込み** | VMware の最近使用した VMX 情報を自動取得。 |

---
## 🎥 デモ動画

[![Demo](assets/demo.png)](assets/demo.mp4)

## 🧩 対応環境

| OS | 状況 |
|----|------|
| 🪟 Windows | ✅ 対応 |
| 🐧 Linux / 🍎 macOS | ⚠️ 現在非対応 |

---

## 📦 インストール方法

1. Python 3.10 以上をインストール  
2. このリポジトリをクローン：

   ```bash
   git clone https://github.com/kyusumya/vmx-manager.git
   cd vmx-optimizer
   ```

3. 依存パッケージをインストール：

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ 使い方

1. 以下のコマンドでツールを起動：

   ```bash
   python main.py
   ```

2. メニューが表示されます。  
   例：

   ```
   📂 VMX Source: preferences.ini

   Select menu:
   > Optimize VM
     VM Spoofing
     Check Status
     Settings
     Exit
   ```

3. 矢印キーで選択、`Enter` で決定します 🎯  

---

## 🌐 言語設定

| コード | 言語 |
|--------|------|
| `ja` | 🇯🇵 日本語 |
| `en` | 🇺🇸 英語 |

メニューの「⚙️ Settings」→「Language」から変更可能です。

---

## 🧰 ファイル構成

```
project/
├─ main.py                 # エントリーポイント
└─ src/
   ├─ ui.py                # CLI / GUI メニュー
   ├─ lang.py              # 言語管理
   ├─ preferences.py       # preferences.ini 解析
   ├─ vmx_config.py        # VMX 設定適用
   ├─ vmx_utils.py         # VMX 読み書きユーティリティ
```

---

## 🛠️ 今後の予定

- [ ] Linux / macOS 対応  
- [ ] GUI モード強化  
- [ ] 設定バックアップ / 復元機能  

---
