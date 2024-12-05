import keyboard
import time

print("打字(文字内容, 打字速度(字每分钟), 等待时间(秒)")
print("需要安装pip install keyboard")
print("""
准确度高：
500精确498
1000精确988
2000精确1936
5000精确4715
10000精确8973
20000精确16703
50000精确33395
100000已经崩溃
""")


def dazi(text, apm, sleep):
    # 计算每个按键的间隔时间（秒）
    interval = 60 / apm
    time.sleep(sleep)  # 等待指定的时间
    for char in text:
        keyboard.press_and_release(char)  # 模拟单击按键
        time.sleep(max(interval, 0.0001))  # 确保间隔时间不低于0.0001秒