import tkinter as tk
import time
import datetime
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageTk import PhotoImage
import json


class APP():
    def __init__(self, trans_color, config, ScaleFactor, restart=None):
        '''
        restart: 重启函数，但是不包括退出函数
        '''
        self.Target = config['Target']
        self.date = config['date']
        self.endtime = datetime.datetime.strptime(self.date,
                                                  '%Y-%m-%d').timestamp()
        self.color = config['color']
        self.fontsize = config['fontsize']
        self.resolution = config['resolution']
        self.trans_color = trans_color
        if restart:
            self.restart = restart
        self.window = tk.Tk()
        # 设置缩放因子
        self.window.tk.call('tk', 'scaling', ScaleFactor / 65)
        # 设置窗口大小以及位置
        self.window.geometry(self.resolution + '-0-0')
        # 设置 ctrl 监听全局变量
        self.window.ctrl_pressed = False
        print(self.window.ctrl_pressed)

        self.set_Line()
        self.set_text()
        self.set_others()
        self.set_layout()
        # 获取并更新时间
        self.get_time()

    def set_Line(self):
        self.CanvasBg = tk.Canvas(self.window,
                                  bg=self.trans_color,
                                  width=self.resolution.split('x')[0],
                                  height=self.resolution.split('x')[1],
                                  highlightthickness=0)
        self.CanvasBg.place(x=0, y=0)
        # self.CanvasBg.create_line(0, 73, 405, 73, fill='white')
        # self.CanvasBg.create_line(0, 150, 405, 200, fill='white')

    def set_text(self):
        self.title_image = create_text_image(
            f'For {self.Target}', "../font/Montserrat-SemiBoldItalic.ttf",
            self.fontsize * 2, self.color)

        self.LabelTitle = tk.Label(self.window,
                                   image=self.title_image,
                                   bg=self.trans_color)

        self.LabelTimes = tk.Label(self.window,
                                   text='00 Days 00 Hours 00 Mins Left',
                                   bg=self.trans_color,
                                   fg=self.color,
                                   font=('Montserrat SemiBold',
                                         round(self.fontsize * 0.618)))
        self.LabelS = tk.Label(
            self.window,
            text='Totally 00 Seconds',
            bg=self.trans_color,
            fg=self.color,
            font=('Montserrat SemiBold',
                  round(self.fontsize *
                        0.618)))  # 使用after方法每1000毫秒（1秒）调用update_timer方法用于更新UI

    def set_layout(self):
        tk.Label(self.window,
                 bg=self.trans_color).pack(expand='yes')  # 仅用来占地方，避免其它控件位置过于靠上
        self.LabelTitle.pack(expand='false')
        self.LabelTimes.pack(expand='false')
        self.LabelS.pack(expand='false')
        tk.Label(self.window,
                 bg=self.trans_color).pack(expand='yes')  # 仅用来占地方，避免其它控件位置过于靠下

    # 设置窗口属性和控件功能
    def set_others(self):
        self.window.resizable(0, 0)  # 固定窗口大小，不可调整
        self.window.overrideredirect(True)  # 去除窗口标题栏
        self.window.focus_force()  # 设置窗口强制焦点
        self.LabelTitle.bind("<Control-Button-1>",
                             self.update_window)  # 绑定鼠标左击事件，用于修改目标
        Hover(self.window, self.LabelTitle, "Config", self.trans_color,
              self.color)
        self.LabelTimes.bind("<Control-Button-1>",
                             self.quit)  # 绑定鼠标左击事件，用于退出程序
        Hover(self.window, self.LabelTimes, "Quit", self.trans_color,
              self.color)
        if self.restart:
            self.LabelS.bind("<Control-Button-1>",
                             self.restart_with_quit)  # 绑定鼠标左击事件，用于重启程序
            Hover(self.window, self.LabelS, "Restart", self.trans_color,
                  self.color)

    def get_time(self):
        s = self.endtime - int(time.time())
        days = int(s / 86400)
        hours = int((s % 86400) / 3600)
        mins = int((s % 3600) / 60)
        self.update_text(days, hours, mins, round(s))
        self.window.after(1000, self.get_time)

    # 更新时间文本，目标文本的更新在 update 函数中
    def update_text(self, days, hours, mins, s):
        self.LabelTimes.config(
            text=f'{days} Days {hours} Hours {mins} Mins Left',
            fg=self.color,
            font=('Montserrat SemiBold', round(0.618 * self.fontsize)))
        self.LabelS.config(text=f'Totally {format(s,",")} Seconds',
                           fg=self.color,
                           font=('Montserrat SemiBold',
                                 round(self.fontsize * 0.618)))

    # 绘制子窗口
    def update_window(self, event=None):
        self.UpdataWindow = tk.Toplevel()
        self.UpdataWindow['bg'] = '#f6ccb4'
        self.UpdataWindow.title('REVISE')
        self.UpdataWindow.geometry('450x279')

        # 创建一个Frame作为容器来存放所有的输入和标签
        frame = tk.Frame(self.UpdataWindow, bg='#f6ccb4')
        frame.pack(expand=True)  # 使得frame居中

        self.EntryTarget = tk.Entry(frame)  # 目标输入框
        self.EntryEndtime = tk.Entry(frame)  # 时间截输入框
        self.EntryColor = tk.Entry(frame)  # 颜色输入框
        self.EntryFontsize = tk.Entry(frame)  # 字体大小输入框

        tk.Label(frame, bg='#f6ccb4', text='TARGET').grid(row=1,
                                                          column=1,
                                                          pady=10,
                                                          padx=5,
                                                          sticky='EW')
        self.EntryTarget.grid(row=1, column=2, sticky='EW')
        tk.Label(frame, bg='#f6ccb4', text='Date').grid(row=2,
                                                        column=1,
                                                        pady=10,
                                                        padx=5,
                                                        sticky='EW')
        self.EntryEndtime.grid(row=2, column=2, sticky='EW')
        tk.Label(frame, bg='#f6ccb4', text='Color').grid(row=3,
                                                         column=1,
                                                         pady=10,
                                                         padx=5,
                                                         sticky='EW')
        self.EntryColor.grid(row=3, column=2, sticky='EW')
        tk.Label(frame, bg='#f6ccb4', text='Fontsize').grid(row=4,
                                                            column=1,
                                                            pady=10,
                                                            padx=5,
                                                            sticky='EW')
        self.EntryFontsize.grid(row=4, column=2, sticky='EW')
        # 修改按钮
        tk.Button(frame,
                  bg=self.trans_color,
                  fg='white',
                  width='19',
                  text='REVISE',
                  command=self.update).grid(row=5,
                                            column=1,
                                            columnspan=2,
                                            sticky='EW')
        print(self.window.ctrl_pressed)

    # 用于将修改更新到父窗口
    def update(self):
        if self.EntryColor.get():
            self.color = self.EntryColor.get()
            self.title_image = create_text_image(
                f'For {self.Target}', "../font/Montserrat-SemiBoldItalic.ttf",
                self.fontsize * 2, self.color)
            # 要求得到self.trans_color 为 color '#FFFFFF'的十六进制值减一
            self.trans_color = '#' + hex(int(self.color[1:], 16) - 1)[2:]
            self.LabelTitle.config(image=self.title_image)
        if self.EntryTarget.get():
            self.Target = self.EntryTarget.get()
            self.title_image = create_text_image(
                f'For {self.Target}', "../font/Montserrat-SemiBoldItalic.ttf",
                self.fontsize * 2, self.color)
            self.LabelTitle.config(image=self.title_image)

        if self.EntryEndtime.get():
            self.date = self.EntryEndtime.get()
            self.endtime = datetime.datetime.strptime(
                self.EntryEndtime.get(), '%Y-%m-%d').timestamp()  # 获取时间截数值
        if self.EntryFontsize.get():
            self.fontsize = int(self.EntryFontsize.get())
        self.UpdataWindow.destroy()  # 销毁子窗口
        self.save_config()

    # 保存配置
    def save_config(self):
        with open('../config/config.json', 'w', encoding='utf8') as f:
            json.dump(
                {
                    'resolution': self.resolution,
                    'Target': self.Target,
                    'date': self.date,
                    'color': self.color,
                    'trans_color': self.trans_color,
                    'fontsize': self.fontsize
                }, f)  # 保存到本地

    # 退出程序
    def quit(self,
             event=None):  # event=None makes the event parameter optional
        self.window.quit()
        self.window.destroy()

    # 重启程序
    def restart_with_quit(self, event=None):
        self.window.quit()
        self.window.destroy()
        self.restart()


# crtl + 鼠标悬停后显示提示框的类
class Hover():
    def __init__(self, root, binded_label, text, bg, fg):
        self.root = root
        self.binded_label = binded_label
        self.tooltip_label = tk.Label(root, text=text, bg=bg, fg=fg)
        self.set_events()

    def set_events(self):
        self.binded_label.bind('<Enter>', self.on_enter)
        self.binded_label.bind('<Leave>', self.on_leave)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)

    def on_enter(self, event):
        if self.root.ctrl_pressed:
            self.tooltip_label.place(x=event.x_root, y=event.y_root)

    def on_leave(self, event=None):
        self.tooltip_label.place_forget()

    def on_key_press(self, event):
        if event.keysym == 'Control_L':
            self.root.ctrl_pressed = True

    def on_key_release(self, event):
        if event.keysym == 'Control_L':
            self.root.ctrl_pressed = False


def create_text_image(text, font_path, font_size, text_color, output_scale=1):
    # 设置为超采样大小的字体
    font = ImageFont.truetype(font_path, font_size * output_scale)
    size = font.getsize(text)
    # 创建透明背景的图像
    image = Image.new('RGBA', size, (0, 0, 0, 0))  # Completely transparent
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=text_color)
    if output_scale > 1:
        # 缩小图像以提高质量
        image = image.resize(
            (size[0] // output_scale, size[1] // output_scale),
            Image.ANTIALIAS)  # 使用替代的Image.ANTIALIAS
    return PhotoImage(image)  # 返回PhotoImage对象
