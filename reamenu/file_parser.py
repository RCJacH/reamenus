import pathlib
import re


spaces_re = re.compile(r'(^ +)')


class FileParser(object):
    def __init__(self, filepath):
        self.path = pathlib.Path(filepath)
        suffixes = self.path.suffixes
        self.name = self.path.stem.split('.')[0]
        self.title = self.name
        if len(suffixes) > 1:
            self.lang = suffixes[0][1:]
        else:
            self.lang = 'en'

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as opened_file:
            self.current_submenu_level = 0
            self.menu_items = []
            for each_line in opened_file.readlines():
                list_item = self.parse_line(each_line)
                if not list_item:
                    continue
                self.menu_items += list_item
            if self.current_submenu_level > 0:
                self.menu_items.append('-3')
                self.current_submenu_level = 0
        final_list = [f'item_{i}={v}' for i, v in enumerate(self.menu_items)]
        return (f'[{self.name}]',) + final_list + (f'title={self.title}',)

    def parse_line(self, line):
        submenu_level = spaces_re.match(line)
        line = line.strip()
        if line[:2] == '# ':
            self.title = line.lstrip('# ')
            return
        elif line == '---':
            list_item = ('-1',)
        elif line[:2] == '##':
            list_item = (f'-4{line.lstrip("#")}',)
        elif line[0] == '>':
            list_item = (f'-2{line[1:]}',)
        else:
            current_level = self.current_submenu_level
            try:
                new_level = submenu_level.end(0)
            except AttributeError:
                new_level = 0
            list_item = (line,)
            if new_level < current_level:
                list_item = ('-3', line)
            self.current_submenu_level = new_level
        return list_item
