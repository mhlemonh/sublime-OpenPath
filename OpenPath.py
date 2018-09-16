import re
import os
import sublime
import sublime_plugin

class OpenPathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.parse_replacement_ketword()
        paths = self.get_selected_path()
        for path in paths:
            self.view.window().open_file(path)

    def get_selected_path(self):
        paths = []
        for region in self.view.sel():
            if region.empty():
                continue
            selected_str = self.replace_define(self.view.substr(region).strip())
            if not os.path.exists(selected_str):
                sublime.error_message("Path does not exist!\n{}".format(selected_str))
                continue
            if not os.access(selected_str, os.R_OK):
                sublime.error_message("Permission denied.")
            else:
                paths.append(selected_str)
        return paths

    def parse_replacement_ketword(self):
        region = sublime.Region(0, self.view.size())
        full_content = self.view.substr(region)
        regex_rules = sublime.load_settings('OpenPath.sublime-settings').get("replacement_regex")
        self.replacement = {"~":os.path.expanduser("~")}
        for regex_rule in regex_rules:
            define_re = re.compile(regex_rule)
            for key, value in define_re.findall(full_content):
                self.replacement[key] = value

    def replace_define(self, selected_string):
        for key in self.replacement:
            if key in selected_string:
                return self.replace_define(selected_string.replace(key, self.replacement[key]))
        else:
            return selected_string
