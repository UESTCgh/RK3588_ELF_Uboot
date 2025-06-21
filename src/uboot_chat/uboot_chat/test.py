from speechGC import Speech

speech = Speech()

print("请按下键盘上的 1、2、3、4（按 ESC 退出）")

while True:
    key = input("按下键盘上的数字键（1-5）或 C 键：")
    if key == '1':
        print("你按下了键 1")
        speech.talk('好的，这就去A1006号房间')
    elif key == '2':
        print("你按下了键 2")
        speech.talk('已到达目标房间，请问有什么需要帮助的吗？')
    elif key == '3':
        print("你按下了键 3")
        speech.talk('好的，这就去A1009号房间')
    elif key == '4':
        print("你按下了键 4")
        speech.talk('已到达目标房间，请问有什么需要帮助的吗？')
    elif key == '5':
        print("你按下了键 5")
        speech.talk('好的，开始返回服务点')
    elif key == 'f':
        print("检测到 ESC，退出程序。")
        break
