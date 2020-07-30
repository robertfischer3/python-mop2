import os
from contextlib import contextmanager


@contextmanager
def change_dir(destination):
    # Allows for temporary change of working directory when used with a with statement
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)
