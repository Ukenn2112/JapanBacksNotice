# Japan Backs Notice
> 日本銀行の残高変動通知と迅速な記帳

## 機能

  Bark + [ショートカット](https://www.icloud.com/shortcuts/f6611bf02c644c15aedff04552d6384f) + [iCost](https://apps.apple.com/jp/app/icost-%E8%AE%B0%E8%B4%A6-%E5%BF%AB%E9%80%9F%E7%AE%80%E6%B4%81%E5%A5%BD%E7%94%A8%E7%9A%84%E7%90%86%E8%B4%A2%E5%8A%A9%E6%89%8B/id1484262528) を使用して、リアルタイムの残高通知と素早い記帳を実現する
  
  <img src="https://user-images.githubusercontent.com/60847880/224486037-63ff15b8-adec-4179-b3ee-1c25fe41e749.gif" align="center" width="200">


## サポート銀行

  - SMBC 三井住友銀行
  - 三菱 UFJ 銀行

## 使用

- ファイルの接尾辞を `data/config.example.yaml` から `data/config.yaml` に変更する

  ファイル内の指示に従って、`config.yaml` 設定ファイルを変更する

- 依存関係とインストール

  ```shell
  pip3 install -r requirements.txt
  ```

  Playwrightを初めてインストールする場合は、`playwright install` を実行する

- 実行

  ```shell
  python3 main.py
  ```
