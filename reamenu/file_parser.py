import math
import pathlib
import re


spaces_re = re.compile(r'(^ +)')


class BaseParser(object):
    def __init__(self, filepath):
        self.path = pathlib.Path(filepath)
        suffixes = self.path.suffixes
        self.name = self.path.stem.split('.')[0]
        self.title = self.name
        if len(suffixes) > 1:
            self.lang = suffixes[0][1:]
        else:
            self.lang = 'en'
        self.is_mixin = 'mixins' in self.path.parts
        self.current_submenu_level = 0

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as opened_file:
            return self.parse(opened_file)

    def parse(self, opened_file):
        return opened_file.read()


def parse_mixin(filepath, lang='en'):
    if lang == 'en':
        lang = ''
    else:
        lang = f'.{lang}'
    parser = BaseParser(f'{filepath}{lang}.txt')
    return parser().split('\n')


class FileParser(BaseParser):
    def parse(self, opened_file):
        self.menu_items = self.parse_lines(opened_file.readlines())
        final_list = [f'[{self.name}]']
        final_list += [f'item_{i}={v}' for i, v in enumerate(self.menu_items)]
        final_list += [f'title={self.title}']
        return final_list

    def parse_lines(self, lines):
        menu_items = []
        current_submenu_level = 0
        for each_line in lines:
            list_item = self.parse_line(each_line)
            if not list_item:
                continue
            elif isinstance(list_item, str):
                list_item = (list_item,)
            back_count, current_submenu_level = self.get_back_count(
                each_line, current_submenu_level,
            )
            menu_items += ('-3',) * back_count + list_item
        if current_submenu_level > 0:
            menu_items.append('-3')
            current_submenu_level = 0
        return menu_items

    def get_back_count(self, line, current_level):
        submenu_level = spaces_re.match(line)
        try:
            new_level = submenu_level.end(0)
        except AttributeError:
            new_level = 0
        return math.ceil((current_level - new_level) / 4), new_level

    def parse_line(self, line):
        if not line:
            return None
        line = line.strip()
        list_item = None
        if line[:2] == '# ':
            self.title = line.lstrip('# ')
        elif line[:2] == '! ':
            self.name = line.lstrip('! ')
        elif line[:8] == '@import ':
            filepath = self.path / '..' / 'mixins' / line.lstrip('@import ')
            list_item = tuple(self.parse_lines(parse_mixin(filepath)))
        elif line == '---':
            list_item = '-1'
        elif line[:2] == '##':
            list_item = f'-4{line.lstrip("#")}'
        elif line[0] == '>':
            list_item = f'-2{line[1:]}'
        else:
            list_item = line
        return list_item
