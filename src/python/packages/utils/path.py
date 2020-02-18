# -*- coding: utf-8 -*-

from os.path import dirname, abspath, basename, extsep


def path_splitter(path):
    """
    Sépare un chemin en trois composantes.

    :param path: le chemin à traiter
    :return: dirpath, name, extension
    """

    dirpath = dirname(abspath(path))
    filename = basename(path)
    result = filename.rsplit(extsep, 1)
    name, ext = '', ''

    if len(result) == 2:
        name, ext = result
    else:
        name = result[0]

    return dirpath, name, ext
