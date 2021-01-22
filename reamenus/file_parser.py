import math
import pathlib
import re


spaces_re = re.compile(r'(^ +)')
increment_re = re.compile(r'{{([\d|-]+)}}')


SRC_PATH = pathlib.Path(__file__).parent.parent / 'src'


class FileParser(object):
    def __init__(self, filepath='', lang='en'):
        self.path = pathlib.Path(filepath)
        self.name = self.path.stem.split('.')[0]
        self.title = None
        self.lang = lang
        self.is_mixin = 'mixins' in self.path.parts

        self.mapper = {
            '#': self.update_title,
            '!': self.update_name,
            '@import': self.mixin,
            '##': lambda x: (f'-4 {x}',),
            '>': lambda x: (f'-2 {x}',),
            '---': lambda *_: ('-1',),
            '++': self.incremental,
        }
        self.menu_items = []
        self.current_indents = 0

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as opened_file:
            return self.parse(opened_file.readlines())

    def parse(self, lines):
        self.parse_lines(lines)
        return self.menu_items if self.is_mixin else self.finalize()

    def finalize(self):
        if not self.title:
            self.title = self.name
        final_list = [f'[{self.name}]', f'title={self.title}']
        final_list += [f'item_{i}={v}' for i, v in enumerate(self.menu_items)]
        return final_list

    def parse_lines(self, lines):
        for each_line in lines:
            self.add_items(each_line)
        self.finalize_indentation()

    def add_items(self, line):
        list_item = self.parse_line(line)
        if not list_item:
            return
        back_count = self.get_back_count(line)
        self.menu_items += ('-3',) * back_count
        self.menu_items += list_item

    def get_back_count(self, line):
        current_indents = self.current_indents
        indents = spaces_re.match(line)
        try:
            new_indents = indents.end(0)
        except AttributeError:
            new_indents = 0
        self.current_indents = new_indents
        return math.ceil((current_indents - new_indents) / 4)

    def parse_line(self, line):
        line = line.strip()
        try:
            line_markup, line_content = line.split(' ', 1)
        except ValueError:
            line_markup, line_content = line, None

        try:
            func = self.mapper[line_markup]
        except KeyError:
            line_content = line
            func = self.other
        return func(line_content)

    def finalize_indentation(self):
        if self.current_indents > 0:
            self.menu_items.append('-3')
            self.current_indents = 0

    def update_title(self, line):
        self.title = line

    def update_name(self, line):
        self.name = line

    def mixin(self, line):
        mixin_file = (
            SRC_PATH / self.lang / 'mixins' / f'{line}.txt'
        )
        parser = FileParser(mixin_file, self.lang)
        return parser()

    def incremental(self, line):
        reps, line_content = line.split(' ', 1)
        content_list = []
        for i in range(int(reps)):
            list_line = increment_re.sub(
                lambda x: self.incremental_repl(x, i), line_content,
            )
            content_list.append(list_line)
        return content_list

    def incremental_repl(self, matchobj, i):
        matched = matchobj.group(1)
        try:
            number, step = matched.split('|')
        except ValueError:
            number = matched
            step = 1
        else:
            step = int(step)
        digits = len(number)
        padded = number[0] == '0'
        final_number = int(number) + i * step
        if padded:
            return f'{str(final_number).zfill(digits)}'
        return str(final_number)

    def other(self, line):
        return (line,) if isinstance(line, str) else line
