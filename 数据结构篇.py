import numpy as np

# 1. 准备地图
# [笔记] dtype=int 强制使用整数，否则默认是 float (带小数点)
room_map = np.zeros((5, 5), dtype=int)


# 2. 定义机器人图纸 (Class)
class Robot:
    # [笔记] __init__ 是出生时自动执行的初始化
    # 🔥🔥 [纠错] 之前没写 icon=9，导致伊娃出生后还是默认的 8
    def __init__(self, name, x=2, y=2, icon=8):
        self.name = name
        self.x = x
        self.y = y  # 🔥🔥 [纠错] 曾漏写 self.y=0，导致移动时报错 "no attribute 'y'"
        self.icon = icon

    def step_up(self):
        # 1. 擦除脚印
        room_map[self.y, self.x] = 0

        # 2. 移动坐标 (y-1 是向上)
        self.y = self.y - 1

        # 3. 标记新位置
        # 🔥🔥 [纠错] 曾写死 room_map[...] = 8
        # 修正：改成 = self.icon，这样伊娃就是 9，瓦力就是 8
        room_map[self.y, self.x] = self.icon

        # 🔥🔥 [纠错] 曾写成 print(print(...))，导致输出 None
        # 修正：去掉外层的 print
        print(f"{self.name} 向上走了一步！")


# 3. 制造机器人 (Object)
# 🔥🔥 [纠错] 实例化时如果不传 icon=9，它就会用默认值 8
bot1 = Robot("瓦力", 0, 0)
bot2 = Robot("伊娃", 4, 4, icon=9)

# 4. 矩阵操作
print("--- 初始地图 ---")
room_map[bot1.y, bot1.x] = bot1.icon
room_map[bot2.y, bot2.x] = bot2.icon

# 🔥🔥 [纠错] 曾写成 print("room_map") 加了引号
# 结果：打印了字母，而不是矩阵数据。修正：去掉引号。
print(room_map)

# 5. 魔法棒 (布尔索引)
# [笔记] 瞬间把所有等于 5 的垃圾变成 0
# room_map[room_map == 5] = 0