# coding:utf8
import json
import os
import random

from scrapy.utils import project

__author__ = 'pangguangde'


class ResUtil(object):
    def __init__(self):
        self.path = self._script_path()
        try:
            self.settings = project.get_project_settings()  # get settings
            self.configPath = self.settings.get("RESOURCE_DIR")
        except:
            pass
        if 'configPath' in self.__dict__:
            self.path = self.configPath

    @staticmethod
    def _script_path():
        import inspect
        this_file = inspect.getfile(inspect.currentframe())
        return os.path.abspath(os.path.dirname(this_file))

    def json_loader(self, res_name):
        with open(self.configPath + os.path.sep + res_name, 'r') as f:
            data = json.load(f)
        f.close()
        return data

if __name__ == '__main__':
    ResUtil().json_loader('user_agent.json')

