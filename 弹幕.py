import tkinter as tk
import random
import time

# 定义提示文本和颜色，与原代码相同
TEXTS = ['记得加衣!', '记得照顾好自己', '天天开心', '好好吃饭', '早点休息', '别感冒']
BG_COLORS = ['pink', 'Lightskyblue', 'lavender', 'lightyellow', 'Darkviolet', 'lightgreen', 'orange']

# 窗口计数器和总数
WINDOW_COUNT = 0
MAX_WINDOWS = 700


def create_popup(root):
    global WINDOW_COUNT

    # 检查是否达到最大数量
    if WINDOW_COUNT >= MAX_WINDOWS:
        # 可以选择在所有窗口创建完毕后关闭主窗口
        # root.quit()
        return

    # 使用 Toplevel 代替 tk.Tk()，更轻量级
    window = tk.Toplevel(root)

    # 获取屏幕尺寸，用于随机定位
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # 随机选择位置、文本和背景色
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    text = random.choice(TEXTS)
    bg = random.choice(BG_COLORS)

    # 设置窗口标题和随机位置
    window.title('天气冷')
    # 窗口尺寸固定为 220x50，然后定位到 (x, y)
    window.geometry(f"220x50+{x}+{y}")

    # 设置窗口为始终在最上层 (可选，增强“弹幕”效果)
    # window.attributes("-topmost", True)

    # 避免子窗口出现在任务栏（可选）
    # if WINDOW_COUNT > 0:
    #     window.transient(root)

    # 创建标签并显示
    tk.Label(
        window,
        text=text,
        bg=bg,
        font=('楷体', 18),
        width=25,
        height=4
    ).pack()

    WINDOW_COUNT += 1

    # 每 10 毫秒（0.01秒）创建下一个窗口，保持原代码的启动频率
    root.after(10, create_popup, root)


def main():
    # 1. 创建一个隐藏的根窗口 (作为所有 Toplevel 窗口的父级)
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口，只显示 Toplevel 弹窗
    root.title("弹幕控制器")

    # 2. 启动第一个窗口的创建，然后利用 after 机制连锁创建后续窗口
    create_popup(root)

    # 3. 启动事件循环 (只启动一次)
    root.mainloop()


if __name__ == '__main__':
    main()