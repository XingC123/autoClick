from tkinter.font import Font
# 重要配置
rootconfig = 'rootconfig'
startwithboot = 'startwithboot'
# 自动点击
autoclick = 'autoclick'
autoclick_interval = 'autoclick_interval'
# 动作列表
action_list = 'action_list'
# 动作类型: 点击/输入 -> click/click_blank/input
action_mode = 'action_mode'
action_x = 'action_x'
action_y = 'action_y'
input_content = 'input_content'
# 单个动作的对象
click_object = 'click_object'

# 文件中部分section名称
userconfig = 'userconfig'


# 字体
class CustomFont:
    def __init__(self):
        font_size = 10
        self.microsoft_yahei_10 = Font(family='microsoft yahei', size=font_size)
