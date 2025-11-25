import random
import time

# 1. 定义字典 (地图与状态)
# [笔记] 字典要用冒号 : 而不是等号 =
robot = {
    "id": "9527",
    "battery": 100,  # 🔥🔥 [纠错] 之前误写成 =，导致语法错误
    "x": 0,
    "y": 0
}


# 2. 定义函数 (动作)
def move():
    # 随机决定方向
    direction = random.randint(0, 1)  # 0是X轴, 1是Y轴
    step = random.choice([-1, 1])  # -1是后退, 1是前进

    if direction == 0:
        robot["x"] += step
    else:
        robot["y"] += step

    # 扣除电量
    robot["battery"] -= 5

    # [笔记] f-string 格式化字符串，% 只是普通文字符号
    print(f"移动中... 抵达坐标 ({robot['x']}, {robot['y']})")


def clean():
    dirt = random.randint(1, 100)
    if dirt > 80:
        print(f"*** 发现灰尘 (等级{dirt})，强力清扫中！ ***")


# 3. 主程序循环
# 🔥🔥 [纠错] 曾忘记加括号调用函数 charge_battery()，导致函数不执行
print("--- 全自动巡航开始 ---")

# 🔥🔥 [纠错] 曾写成 while "battery" > 0
# 原因：不能拿字符串 "battery" 和数字 0 比大小。
# 修正：必须用 robot["battery"] 取出里面的数字。
while robot["battery"] > 0:
    # 🔥🔥 [纠错] 曾写成 for clean_spot in range(5)
    # 原因：循环变量名和函数名冲突，导致函数变成了数字。
    # 修正：循环变量用 i，函数调用要加括号 clean()
    move()
    clean()

    print(f"剩余电量：{robot['battery']}%")
    print("----------------")
    time.sleep(1)  # [笔记] time库的使用：让程序暂停 1 秒

print("电量耗尽，自动关机。")