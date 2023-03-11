# Japan Backs Notice
> 日本银行余额变动通知及快速记账

## 功能

  利用 Bark + 快捷指令 + iCost 实现实时余额通知以及快速记账
  
  <img src="https://user-images.githubusercontent.com/60847880/224486037-63ff15b8-adec-4179-b3ee-1c25fe41e749.gif" align="center" width="200">


## 支持银行

  - SMBC 三井住友銀行

## 使用

- 修改文件后缀 `data/config.example.yaml` 为 `data/config.yaml`

  根据文件内提示修改 `config.yaml` 配置文件

- 安装依赖

  ```shell
  pip3 install -r requirements.txt
  ```

  首次安装 `playwright` 执行 `playwright install`

- 运行

  ```shell
  python3 main.py
  ```
