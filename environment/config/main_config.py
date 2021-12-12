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
        print('main_app_execute_path = ', main_app_execute_path)
        main_config_abspath = os.path.join(main_app_execute_path, main_config_name)
        # 本类属性
        self.config_path = main_config_abspath
        self.main_config = None
        if self.read_config() is False or len(self.get_sections()) == 0:
            # self.add_section(userconfig)
            self.add_section(rootconfig)

        # 程序运行重要配置
        self.root_config = None

    def read_config(self):
        if os.path.exists(main_config_abspath):
            self.main_config = None
            self.main_config = configparser.ConfigParser()
            self.main_config.read(main_config_abspath, encoding='utf-8')
            if len(self.get_sections()) != 0:
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

    def clear(self):
        with open(main_config_abspath, 'w', encoding='utf-8') as f:
            f.write('')
        self.main_config = None
        self.add_section(userconfig)
