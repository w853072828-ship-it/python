import numpy as np

# 1. 地图设置
room_map = np.zeros((5, 5), dtype=int)
room_map[1:4, 1] = 1  # 切片设置墙壁
start = (0, 0)
target = (4, 4)
room_map[target] = 9

# [笔记] map_data.shape 返回 (行数, 列数)，用于动态判断边界
rows, cols = room_map.shape

# 2. 初始化算法
# [笔记] Queue (列表) 用于排队，Set (集合) 用于防止走回头路
queue = [start]
came_from = {}  # 既能记账(visited)，又能记录"谁带我来的"
came_from[start] = None

print(f"--- 开始从 {start} 前往 {target} ---")

found = False

while len(queue) > 0:
    current = queue.pop(0)  # 取出队头

    if current == target:
        found = True
        break

    y, x = current

    # [笔记] 解包：直接把元组里的三个值赋给三个变量
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dy, dx in directions:
        next_y, next_x = y + dy, x + dx
        next_pos = (next_y, next_x)

        # 🔥🔥 [纠错] 边界判断
        # 必须确保 0 <= y < rows，否则报错 IndexError
        if 0 <= next_y < rows and 0 <= next_x < cols:
            if room_map[next_y, next_x] != 1:  # 不是墙
                if next_pos not in came_from:  # 没来过

                    # 🔥🔥 [纠错] 曾写成 queue.append(a, b)
                    # 修正：append 只能接一个参数，必须把坐标当做一个整体(元组)传进去
                    queue.append(next_pos)
                    came_from[next_pos] = current  # 记录来源

# 3. 路径回溯
if found:
    curr = target
    while curr != start:
        if curr != target:
            room_map[curr] = 8  # 标记路径
        # 查字典，找上一步
        curr = came_from[curr]

    room_map[start] = 8
    print(room_map)
else:
    print("❌ 无路可走")