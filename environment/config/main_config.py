import configparser
import os.path
from environment.custom_constant.custom_constant import *

# 配置文件属性声明(赋值在MainConfig()的init函数中)
main_config_name = 'autoClick_config.ini'
main_config_abspath = ''


class MainConfig:

    def __init__(self, main_app_execute_path):
        # 为配置文件属性赋值
        global main_config_abspath
        main_config_abspath = os.path.join(main_app_execute_path, main_config_name)
        print('main_config_abspath = ', main_config_abspath)
        # 本类属性
        self.config_path = main_config_abspath
        self.main_config = None
        self.sections = None
        if self.read_config() is False:
            self.main_config = configparser.ConfigParser()
            self.set_value(rootconfig, startwithboot, '')
            self.sections = self.get_sections()

        # 程序运行重要配置
        self.root_config = None

    def read_config(self):
        if os.path.exists(main_config_abspath):
            if self.main_config is not None:
                self.main_config = None
            self.main_config = configparser.ConfigParser()
            self.main_config.read(main_config_abspath, encoding='utf-8')
            self.sections = self.get_sections()
            if len(self.sections) != 0 and self.main_config.has_section(rootconfig):
                return True
        else:
            return False

    def add_section(self, section):
        if self.main_config is None:
            self.main_config = configparser.ConfigParser()
        if self.main_config.has_section(section) is False:
            self.main_config.add_section(section)
            self.main_config.write(open(main_config_abspath, 'w+', encoding='utf-8'))
            return True
        return False

    def set_value(self, section, key, value):
        if not self.main_config.has_section(section):
            self.main_config.add_section(section)
        self.main_config.set(section, key, str(value))
        self.main_config.write(open(main_config_abspath, 'w+', encoding='utf-8'))

    def get_value(self, section, key):
        if self.main_config.has_option(section, key):
            return self.main_config.get(section, key)
        else:
            return ''

    def get_sections(self):
        return self.main_config.sections()

    def get_items(self):
        return self.main_config.items()

    def get_config(self, section):
        # 按照既定格式,以数组形式返回section的items
        # [[自动点击(, 延迟时间)], [动作列表]]
        config_list = []
        # 0号位: [自动点击(, 延迟时间)]
        autoclick_value = self.if_value_exist(self.get_value(section, autoclick))
        config_list.append([])
        if autoclick_value:
            config_list[0].append(autoclick_value)
            config_list[0].append(int(self.get_value(section, autoclick_interval)))
        else:
            config_list[0].append(False)
        # 1号位: [操作列表]
        action_list_value = self.if_value_exist(self.get_value(section, action_list))
        config_list.append([])
        if action_list_value != '':
            config_list[1] = action_list_value
        return config_list

    def delete_section(self, section):
        if self.main_config.has_section(section):
            self.main_config.remove_section(section)
            self.main_config.write(open(main_config_abspath, 'w+', encoding='utf-8'))

    @staticmethod
    def if_value_exist(value):
        # 判断所给函数值是否为空
        if value != '':
            return eval(value)
        return ''

    def clear(self):
        # 清空配置
        with open(main_config_abspath, 'w', encoding='utf-8') as f:
            f.write('')
        self.main_config = None
        self.set_value(rootconfig, startwithboot, '')
