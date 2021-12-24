import environment.custom_constant.custom_constant as custom_constant


class ClickConfig:
    def __init__(self, config_name='', action_list=None):
        if action_list is None:
            action_list = []
        self.config_name = config_name
        self.action_list = action_list

    def generate_click_object(self):
        # 生成
        return [self.config_name, self.action_list]

    @staticmethod
    def print_click_object(action_dic):
        # 打印
        # action_dic = action_list[0]
        result = {}
        if action_dic[custom_constant.action_mode] == custom_constant.input_action:
            result['操作'] = '输入'
            result['内容'] = action_dic[custom_constant.input_content]
        elif action_dic[custom_constant.action_mode] == custom_constant.open_webbroswer_action:
            result['操作'] = '打开网址'
            result['网址'] = action_dic[custom_constant.input_content]
        elif action_dic[custom_constant.action_mode] == custom_constant.open_file_action:
            result['操作'] = '打开文件'
            result['路径'] = action_dic[custom_constant.input_content]
        elif action_dic[custom_constant.action_mode] == custom_constant.click_action:
            result['操作'] = '点击'
        result['坐标'] = (action_dic[custom_constant.action_x], action_dic[custom_constant.action_y])
        return result
