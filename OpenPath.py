import re
import os
import sublime
import sublime_plugin

class OpenPathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.get_define()
        paths = self.get_selected_path()
        for path in paths:
            sublime.set_timeout(lambda: self.view.window().open_file(path, sublime.ENCODED_POSITION), 0)

    def get_selected_path(self):
        paths = []
        for region in self.view.sel():
            if not region.empty():
                selected_str = self.replace_define(self.view.substr(region))
                print(selected_str)
                if os.path.exists(selected_str):
                    paths.append(selected_str)
        return paths

    def get_define(self):
        region = sublime.Region(0, self.view.size())
        full_content = self.view.substr(region)
        define_re = re.compile("#DEFINE\s+(\<\w+\>)\s+([\w\/]+)")
        self.define_dict = {key:value for key, value in define_re.findall(full_content)}

    def replace_define(self, select_string):
        for define_key in self.define_dict:
            if define_key in select_string:
                return select_string.replace(define_key, self.define_dict[define_key])
        return select_string
