import pathlib

from reamenus.file_parser import FileParser


class Finalizer(object):
    def __init__(self, folderpath, lang='en'):
        self.folder = pathlib.Path(folderpath)
        parent = self.folder.parent
        self.src_folder = parent / 'src'
        self.release_folder = parent / 'release'
        self.all_lang = (
            x for x in self.src_folder.iterdir() if x.is_dir()
        )

    def __call__(self):
        for each_lang in self.all_lang:
            self.release_lang(each_lang)

    def release_lang(self, lang):
        release_path = (
            self.release_folder / f'ReaMenus.{lang.name}.ReaperMenuset'
        )
        all_files = sorted(
            self.get_all_files(lang), key=lambda x: x.name.lower()
        )
        with open(release_path, 'w', encoding='utf-8') as release_file:
            all_lines = []
            for each_file in all_files:
                all_lines += each_file()
                all_lines += ('',)
            release_file.write('\n'.join(all_lines))

    def get_all_files(self, lang):
        lang_folder = self.src_folder / lang
        return (
            FileParser(f) for f in lang_folder.rglob(r'*.txt')
            if 'mixins' not in f.parts
        )
