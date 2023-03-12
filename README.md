# Japan Backs Notice
> 日本銀行の残高変動通知と迅速な記帳

## 機能

  Bark + [ショートカット](https://www.icloud.com/shortcuts/f6611bf02c644c15aedff04552d6384f) + iCost を使用して、リアルタイムの残高通知と素早い記帳を実現する
  
  <img src="https://user-images.githubusercontent.com/60847880/224486037-63ff15b8-adec-4179-b3ee-1c25fe41e749.gif" align="center" width="200">


## サポート銀行

  - SMBC 三井住友銀行

## 使用

- ファイルの接尾辞を `data/config.example.yaml` から `data/config.yaml` に変更てください

  ファイル内の指示に従って、`config.yaml` 設定ファイルを変更してください

- 依存関係のインストール

  ```shell
  pip3 install -r requirements.txt
  ```

  Playwrightを再インストールするには、`playwright install` を実行してください

- 実行

  ```shell
  python3 main.py
  ```
