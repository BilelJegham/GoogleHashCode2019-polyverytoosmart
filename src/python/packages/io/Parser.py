# -*- coding: utf-8 -*-

from collections import namedtuple

from packages.structure.Library import Library
from packages.structure.Problem import Problem
from packages.utils.log import log


class Parser:

    @staticmethod
    def load(source_file):
        """
        Parse un fichier-carte et en construit une représentation en mémoire.

        :param source_file: le chemin absolu de la carte à traiter en entrée
        :return: une représentation structurée du problème
        :rtype: Problem
        """

        with open(source_file) as f:

            # informations d'en-tête
            nbBooks, nbLib, day = map(int, f.readline().split())
            booksScore = f.readline().split()
            allBooks = dict()
            for i in range(nbBooks):
                allBooks[i] = int(booksScore[i])

            libs = []
            for i in range(nbLib):
                nbBooks, nbLib, dayl = map(int, f.readline().split())
                booksId = list(map(int, f.readline().split()))

                booksId = sorted(booksId, key=lambda x: allBooks[x], reverse=True)
                l = Library(booksId, nbLib, dayl, 0)
                l.resetRatio(allBooks,day, 0)
                libs.append(l)

            problem = Problem(allBooks, day, libs)

        return problem
