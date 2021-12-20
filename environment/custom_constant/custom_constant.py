from tkinter.font import Font
# 重要配置
rootconfig = 'rootconfig'
startwithboot = 'startwithboot'

# 文件中部分section名称
userconfig = 'userconfig'


# 字体
class CustomFont:
    def __init__(self):
        font_size = 10
        self.microsoft_yahei_10 = Font(family='microsoft yahei', size=font_size)
