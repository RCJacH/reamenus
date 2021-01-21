import pytest

from reamenus.file_parser import FileParser


@pytest.mark.parametrize(
    'filename, name, lang',
    [
        ('case_file.txt', 'case_file', 'en'),
        ('case_file.fr.txt', 'case_file', 'fr'),
        ('case_file.zh-cn.txt', 'case_file', 'zh-cn'),
    ],
)
def test_init(filename, name, lang):
    parser = FileParser(filename)
    assert parser.name == name
    assert parser.lang == lang


def test_parse_title():
    parser = FileParser()
    parser.parse_line('# title')
    assert parser.title == 'title'


@pytest.mark.parametrize(
    'line, list_item',
    [
        ('## HEADER', ('-4 HEADER',)),
        ('  ## HEADER', ('-4 HEADER',)),
        ('    ## HEADER', ('-4 HEADER',)),
        ('---', ('-1',)),
        ('  ---', ('-1',)),
        ('    ---', ('-1',)),
        ('> subheader', ('-2 subheader',)),
        ('    > subheader', ('-2 subheader',)),
        ('       > subheader', ('-2 subheader',)),
        ('++ 2 a{{1}}', ['a1', 'a2']),
        ('++ 2 a{{1}}_b{{10}}', ['a1_b10', 'a2_b11']),
        ('++ 3 a{{1}}_b{{10|2}}', ['a1_b10', 'a2_b12', 'a3_b14']),
        ('++ 2 a{{17265}}_b{{10|-2}}', ['a17265_b10', 'a17266_b8']),
        ('++ 2 a{{01}}_b{{10}}', ['a01_b10', 'a02_b11']),
        ('++ 2 a{{01}}_b{{10|-2}}', ['a01_b10', 'a02_b8']),
    ],
)
def test_parse_line(line, list_item):
    parser = FileParser()
    assert parser.parse_line(line) == list_item


@pytest.mark.parametrize(
    'lines, list_items',
    [
        (
            ('> Submenu', '    sub item', 'normal_item'),
            ['-2 Submenu', 'sub item', '-3', 'normal_item'],
        ),
        (
            ('> Submenu', '    sub item', '    sub item 2', 'normal_item'),
            ['-2 Submenu', 'sub item', 'sub item 2', '-3', 'normal_item'],
        ),
    ],
)
def test_parse_subtitles(lines, list_items):
    parser = FileParser()
    parser.is_mixin = True
    assert parser.parse(lines) == list_items


def test_parse_file():
    parser = FileParser('tests/case_file.txt')
    assert parser() == [
        '[case_file]',
        'item_0=-4 HEADER',
        'item_1=-1',
        'item_2=-2 Submenu',
        'item_3=Sub item',
        'item_4=-1',
        'item_5=Sub item2',
        'item_6=-2 SubSubmenu',
        'item_7=sub sub item',
        'item_8=-1',
        'item_9=sub sub item2',
        'item_10=-3',
        'item_11=-3',
        'item_12=item',
        'title=Title',
    ]
