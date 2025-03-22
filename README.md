# BPDS
BPDS-幼児うつぶせ検出装置-



###
jikkiブランチがほぼメイン

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
(二台使用する場合は同じネットワークに接続し環境構築を済ませ、検出側でface.py,受信側でkoki.pyを起動する)

face.pyの起動
```sh
python3 ./face.py
```

koki.pyの起動
```
python3 ./oya.py
```

## 機能
### face.py

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
- 顔検出中はface.pyのプロセスに顔の座標が表示され続ける。
- 顔が検出されなくなると通知送信までのカウントダウンが出力され、約5秒経過するとkoki.pyにうつ伏せ検知の通知が送信される。
- face,koki共に検知後も停止しないようになっている

##
