# BPDS
BPDS-幼児うつぶせ検出装置-




oyaki
koki 3.13.2 hi env
### envでの実行用
```sh
cd BPDS/
source venv/bin/activate
sudo venv/bin/python3 main.py
sudo venv/bin/python3 kokit.py
```
## Macでの環境構築

#### 1. 公式からPython3.12.9をインストール

#### 2. リポジトリのクローン
リポジトリをクローンし、cloneしたgitディレクトリに移動する
```sh
git clone https://github.com/shikesyake/BPDS.git && cd BPDS
```

#### 3. モジュールのインストール
pythonモジュールをインストールする
```sh
pip install -r requirements.txt
```
## ubuntuでの環境構築

2番まではMacと同じ手順
### 仮想環境の作成(親機のみ)
BPDS直下でenvを作成する
アクティベートする

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
python3 main.py
```

koki.pyの起動
```sh
python3 koki.py
```

## 機能
### main.py
親機での実行を想定
実行後、顔が一定時間検知され続けるまで待機
待機し顔の検知を行う

### face.py

顔の検出、描画を行う
うつ伏せ時の通知を送信する
実行直後から検出が始まる
### send.py
送受信共用

### koki.py
受信機。
通知を表示する。

実行直後から受信待機状態になる

通知受信時に
tuitade 特に視覚的な変化はしない。
ターミナルには送信元と通知内容が出力される。


### kokit.py
LEDやブザーを持つ機器用の受信機。
基本的にkoki.pyと機能は変わらない。
実行直後から受信待機状態になる

通知受信時に出力される。



### button.py

##
### 注意点
- 接続したWebカメラの画角内に顔を収めた状態で両方実行しないとうつ伏せ検知がkokiに送信される。
- 顔検出中はmain.pyのプロセスに顔の座標が表示され続ける。
- 顔が検出されなくなると通知送信までのカウントダウンが出力され、約5秒経過するとkoki.pyにうつ伏せ検知の通知が送信される。
- main,koki共に検知後も停止しないようになっている
- 2台使用かつkokiから親機への通信もする場合はmain.pyの24行目のコメントアウトを解除する(同一端末で同じアドレスをbindすることはできないため)
##
