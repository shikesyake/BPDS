# BPDS
BPDS-幼児うつぶせ検出装置-

### envでの実行用
cd BPDS/
source venv/bin/activate
sudo venv/bin/python3 main.py
sudo venv/bin/python3 kokit.py

## Macでの環境構築

#### 1. 公式からPython3.12.9をインストール

#### 2. レポジトリのクローン
レポジトリをクローンし、cloneしたgitディレクトリに移動する
```sh
git clone https://github.com/shikesyake/BPDS.git && cd BPDS
```

#### 3. モジュールのインストール
pythonモジュールをインストールする
```sh
pip install -r requirements.txt
```


## 使用方法

### アプリケーションの起動
#### 1. cloneしたgitディレクトリでターミナルを二つ開く
(二台使用する場合は同じネットワークに接続し環境構築を済ませ、検出側でmain.py,受信側でkoki.pyを起動する)

main.pyの起動
```sh
python3 ./main.py
```

koki.pyの起動
```sh
python3 ./koki.py
```

## 機能
### main.py
親機での実行を想定

### face.py

モジュール
顔の検出、うつ伏せ時の通知を送信する

実行直後から検出が始まる

### koki.py
受信機。
通知を表示する。

実行直後から受信待機状態になる

通知受信時に出力される。
##
### 注意点
- 接続したWebカメラの画角内に顔を収めた状態で両方実行しないとうつ伏せ検知がkokiに送信される。
- 顔検出中はmain.pyのプロセスに顔の座標が表示され続ける。
- 顔が検出されなくなると通知送信までのカウントダウンが出力され、約5秒経過するとkoki.pyにうつ伏せ検知の通知が送信される。
- main,koki共に検知後も停止しないようになっている
- 2台使用かつkokiから親機への通信もする場合はmain.pyの24行目のコメントアウトを解除する(同一端末で同じアドレスをbindすることはできないため)
##
