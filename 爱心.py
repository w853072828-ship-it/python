import tkinter as tk
import random
import math
import queue

# --- 配置区域 ---

# 定义弹窗消息
messages = [
    '多喝热水哦', '每天都要元气满满', '保持好心情', '好好爱自己',
    '梦想成真', '期待下一次见面', '顺顺利利', '早点休息哦',
    '愿所有烦恼都消失', '今天过得开心嘛', '注意保暖哦', '金榜题名',
    '我想你了', '晚安', '你要快乐呀', '加油'
]

# 定义浅色系颜色列表 (马卡龙色系)
colors = [
    # 粉色系
    '#FFB6C1', '#FFC0CB', '#FFE4E1',
    # 红色系
    '#FFA07A', '#FA8072', '#F08080',
    # 橙色系
    '#FFDAB9', '#FFE4B5', '#FFEFD5',
    # 黄色系
    '#FFFACD', '#FFF8DC', '#FFFFE0',
    # 绿色系
    '#98FB98', '#90EE90', '#ADFF2F',
    # 蓝色系
    '#87CEFA', '#ADD8E6', '#B0E0E6',
    # 紫色系
    '#DDA0DD', '#E6E6FA', '#D8BFD8',
    # 青色系
    '#AFEEEE', '#E0FFFF', '#F0FFFF'
]


class PopupManager:
    def __init__(self):
        # 创建主窗口但不显示
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口，只显示弹窗

        # 创建任务队列
        self.task_queue = queue.Queue()

        # 存储已创建的窗口引用，防止被垃圾回收
        self.windows = []

        # 获取屏幕尺寸
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # 生成爱心形状的点坐标 (调整位置和大小)
        # 预先计算150个点，对应后面默认的150个弹窗
        self.heart_points = self.generate_heart_points(150)
        self.heart_index = 0

        # 设置定期检查队列 (每100ms检查一次是否有新任务)
        self.root.after(100, self.process_queue)

    def generate_heart_points(self, count):
        """生成从屏幕中心偏上偏左位置开始的爱心形状点坐标，大小适中"""
        points = []

        # 计算缩放因子，使爱心大小适中
        scale_x = self.screen_width / 40  # 增加分母使爱心变小
        scale_y = self.screen_height / 35  # 增加分母使爱心变小
        scale = min(scale_x, scale_y) * 1  # 这里的系数可以调整整体大小

        # 计算爱心中心位置 (屏幕中心偏上偏左)
        # 向左偏移 5%，向上偏移 8%
        heart_center_x = self.screen_width / 2 - self.screen_width * 0.05
        heart_center_y = self.screen_height / 2 - self.screen_height * 0.08

        # 生成爱心点
        for i in range(count):
            # 参数 t 从 0 到 2pi
            t = (i / count) * 2 * math.pi

            # 爱心参数方程
            x = 16 * (math.sin(t) ** 3)
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)

            # 缩放
            x *= scale
            y *= -scale  # 翻转Y轴，因为屏幕坐标系Y向下是正

            # 将爱心中心置于调整后的位置
            x += heart_center_x
            y += heart_center_y

            # 确保坐标在屏幕范围内 (留出适当边距)
            # 简单的边界处理，防止窗口生成在屏幕外太远
            x = max(80, min(self.screen_width - 280, x))
            y = max(80, min(self.screen_height - 180, y))

            points.append((int(x), int(y)))

        return points

    def create_popup(self, random_msg, random_color):
        """在主线程中创建弹窗"""
        try:
            window = tk.Toplevel(self.root)
            window.wm_attributes("-topmost", True)  # 确保窗口在最前

            # 根据文本长度动态计算窗口大小
            text_length = len(random_msg)
            base_width = max(240, min(380, text_length * 11))  # 动态宽度
            base_height = max(75, (text_length // 15) * 18 + 35)  # 动态高度

            # 使用爱心形状的坐标
            if self.heart_index < len(self.heart_points):
                x, y = self.heart_points[self.heart_index]
                self.heart_index += 1
            else:
                # 如果爱心点用完了，就随机位置
                x = random.randrange(80, self.screen_width - base_width - 80)
                y = random.randrange(80, self.screen_height - base_height - 80)

            window.title('亲爱的')
            window.geometry(f"{int(base_width)}x{int(base_height)}+{int(x)}+{int(y)}")
            window.configure(bg=random_color)
            window.resizable(False, False)

            # 禁用关闭按钮 (点X没反应)
            window.protocol("WM_DELETE_WINDOW", lambda: None)

            # 创建框架容器
            frame = tk.Frame(window, bg=random_color)
            frame.pack(expand=True, fill="both", padx=12, pady=12)

            # 使用 Message 组件，支持自动换行
            message = tk.Message(
                frame,
                text=random_msg,
                bg=random_color,
                font=("楷体", 13),  # 字体可根据系统调整，如 "Microsoft YaHei"
                width=base_width - 45,
                justify='center'
            )
            message.pack(expand=True, fill="both")

            # 30秒后自动关闭窗口
            window.after(30000, window.destroy)

            # 存储窗口引用
            self.windows.append(window)

            return window

        except Exception as e:
            print(f"窗口创建错误: {e}")
            return None

    def add_popup_task(self):
        """添加弹窗任务到队列"""
        random_msg = random.choice(messages)
        random_color = random.choice(colors)
        self.task_queue.put(('popup', random_msg, random_color))

    def process_queue(self):
        """处理队列中的任务"""
        try:
            while True:
                try:
                    # 非阻塞获取任务
                    task_type, *args = self.task_queue.get_nowait()

                    if task_type == 'popup':
                        self.create_popup(*args)

                    self.task_queue.task_done()
                except queue.Empty:
                    break
        except Exception as e:
            print(f"处理队列错误: {e}")
        finally:
            # 继续定期检查队列
            self.root.after(100, self.process_queue)

    def start_popups(self, count=150, interval=0.1):
        """启动弹窗序列"""
        for i in range(count):
            # 使用 after 方法在主线程中调度弹窗创建
            # interval 是弹窗出现的间隔时间(秒)
            self.root.after(int(i * interval * 1000), self.add_popup_task)

    def run(self):
        """启动主循环"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"主循环错误: {e}")
        finally:
            # 清理资源
            for window in self.windows:
                try:
                    window.destroy()
                except:
                    pass
            try:
                self.root.quit()
            except:
                pass


def main():
    # 创建弹窗管理器
    manager = PopupManager()

    # 启动弹窗序列 (数量150个，间隔0.1秒)
    manager.start_popups(count=150, interval=0.1)

    # 启动主循环
    manager.run()


if __name__ == "__main__":
    main()