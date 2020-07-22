import os


def get_path_from_root(*args):
    dname = os.path.dirname(os.path.abspath(__file__))  # wb_nlp
    dname = os.path.dirname(dname)  # src
    dname = os.path.dirname(dname)  # wb_nlp

    return os.path.join(dname, *args)


def get_data_dir(*args):
    return get_path_from_root('data', *args)
