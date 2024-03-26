# 在windows系统上写一个桌面倒计时程序
# 源码地址：https://blog.csdn.net/qq_43495412/article/details/113099677
# 分辨率改善：https://blog.csdn.net/qq_25921925/article/details/103987572

import ctypes
import json
from screentimer import APP
import sys
import os
# 调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 调用api获得当前的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


def app_restart(event=None):
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    with open('../config/config.json', 'r', encoding='utf8') as f:
        config = json.load(f)
        trans_color = config['trans_color']
    myapp = APP(trans_color, config, ScaleFactor, app_restart)
    # 设置窗口透明
    myapp.window.wm_attributes('-transparentcolor', trans_color)
    myapp.window.mainloop()
