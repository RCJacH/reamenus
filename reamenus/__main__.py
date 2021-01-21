import os

from reamenus import Finalizer


FILE_PATH = os.path.dirname(__file__)


def main(*args, **kwargs):
    finalizer = Finalizer(FILE_PATH, *args, **kwargs)
    finalizer()


if __name__ == '__main__':
    main()
