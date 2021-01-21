import pathlib

from reamenu.file_parser import FileParser


class Finalizer(object):
    def __init__(self, folderpath, lang='en'):
        self.folder = pathlib.Path(folderpath)
        self.src_folder = self.folder.parent / 'src'
        self.release_path = self.folder.parent / 'release' / 'ReaMenus.ReaperMenuSet'
        self.all_files = [
            x for x in self.get_all_files() if (
                x.lang == lang and not x.is_mixin
            )
        ]

    def __call__(self):
        with open(self.release_path, 'w', encoding='utf-8') as release_file:
            all_lines = []
            for each_file in self.all_files:
                all_lines += each_file()
                all_lines += ('\n',)
            release_file.write('\n'.join(all_lines))

    def get_all_files(self):
        return (FileParser(f) for f in self.src_folder.glob(r'./**/*.txt'))
