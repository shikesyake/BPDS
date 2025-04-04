from send import P2P
import sys
# 定義
P2Psend = P2P()
# バインド
#P2Psend.bind()


def usage():
    print("""
Usage: command [options]

Description: [ファイルの説明]

Features: [ファイルの説明]

Arguments: [引数の説明]

Options:
    -h|--help           Display help
       --help_jp        Display help in Japanese
    -a|--akan           akan送信
    -t|--tomareya       tomareya送信
""")

def alert_func():
    P2Psend.alert()
def stop_func():
    P2Psend.stop_alert()

def sendm_func():
     data = (input("送信するデータを入力してください: "))
     data = data.encode(encoding='utf-8')
     print(f"{data}を送信します")
     P2Psend.send(data)

i = 1
options = set()  # 使用されたオプションを格納するための集合

for i in range(1,len(sys.argv)):
    if sys.argv[i] in ["-h", "--help"]: 
        usage()
        sys.exit(0) # 正常終了する

    elif sys.argv[i] in ["-a", "--akan"]:
        alert_func()
        print("あかんわ")
        i += 1 # 処理を実行した後は、次の引数を処理するためにiに1を足す
        sys.exit(0) # 正常終了する
    
    elif sys.argv[i] in ["-t", "--tomareya"]:
        stop_func() 
        print("はよ止まれや")       
        i += 1 # 処理を実行した後は、次の引数を処理するためにiに1を足す
        sys.exit(0) # 正常終了する
    
    elif sys.argv[i] in ["-m", "--message"]:
        print("意味ないで")  
        sendm_func()
              
        i += 1 # 処理を実行した後は、次の引数を処理するためにiに1を足す
        sys.exit(0) # 正常終了する
    
    elif sys.argv[i].startswith("--"):
        print("\033[91mError: Invalid Option\n無効なオプションです。--help を使用してください。\033[0m")
        sys.exit(1) # 異常終了する

print("""オプション指定しろ 
-a, akanを送信 
-t, tomareyaを送信
-m, 好きな文を送信""")

