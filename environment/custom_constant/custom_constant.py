from tkinter.font import Font
# 重要配置
rootconfig = 'rootconfig'
startwithboot = 'startwithboot'
# 自动点击
autoclick = 'autoclick'
autoclick_interval = 'autoclick_interval'
# 动作列表
action_list = 'action_list'
# 动作类型: 点击/输入 -> click/input
action_mode = 'action_mode'
action_x = 'action_x'
action_y = 'action_y'
input_content = 'input_content'
# 是否点击空白处
click_blank = 'click_blank'
click_blank_x = 'click_blank_x'
click_blank_y = 'click_blank_y'

# 文件中部分section名称
userconfig = 'userconfig'


# 字体
class CustomFont:
    def __init__(self):
        font_size = 10
        self.microsoft_yahei_10 = Font(family='microsoft yahei', size=font_size)
