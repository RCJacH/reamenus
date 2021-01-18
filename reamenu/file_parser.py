import math
import pathlib
import re


spaces_re = re.compile(r'(^ +)')


class FileParser(object):
    def __init__(self, filepath):
        self.path = pathlib.Path(filepath)
        suffixes = self.path.suffixes
        self.name = self.path.stem.split('.')[0]
        self.title = None
        if len(suffixes) > 1:
            self.lang = suffixes[0][1:]
        else:
            self.lang = 'en'
        self.current_submenu_level = 0

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as opened_file:
            self.current_submenu_level = 0
            self.menu_items = self.parse(opened_file.readlines())
            if self.current_submenu_level > 0:
                self.menu_items.append('-3')
                self.current_submenu_level = 0
        final_list = [f'[{self.name}]']
        final_list += [f'item_{i}={v}' for i, v in enumerate(self.menu_items)]
        if self.title:
            final_list += [f'title={self.title}']
        return final_list

    def parse(self, lines):
        menu_items = []
        for each_line in lines:
            list_item = self.parse_line(each_line)
            if not list_item:
                continue
            back_count = self.get_back_count(each_line)
            menu_items += ('-3',) * back_count + (list_item,)
        return menu_items

    def get_back_count(self, line):
        current_level = self.current_submenu_level
        submenu_level = spaces_re.match(line)
        try:
            new_level = submenu_level.end(0)
        except AttributeError:
            new_level = 0
        self.current_submenu_level = new_level
        return math.ceil((current_level - new_level) / 4)

    def parse_line(self, line):
        line = line.strip()
        list_item = None
        if line[:2] == '# ':
            self.title = line.lstrip('# ')
        elif line[:2] == '! ':
            self.name = line.lstrip('! ')
        elif line == '---':
            list_item = '-1'
        elif line[:2] == '##':
            list_item = f'-4{line.lstrip("#")}'
        elif line[0] == '>':
            list_item = f'-2{line[1:]}'
        else:
            list_item = line
        return list_item
