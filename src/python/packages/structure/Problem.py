# -*- coding: utf-8 -*-

from packages.io.Solution import Solution
from packages.solving.Algo import Algo
from packages.utils.log import log



class Problem:
    """
    Représente le problème posé.
    A à sa disposition toutes les informations nécessaires à sa résolution.

    """

    def __init__(self, books, day, libs):
        """
            Constructeur
        """
        self.allBooks = books
        self.day = day
        self.libraries = libs

    def __str__(self):
        representation = str(self.allBooks)
        representation += "\n"+str(self.day)
        for l in self.libraries:
            representation += "\n   "+str(l)

        return representation

    def solve(self):
        """
        Résout le problemes en plaçant les routeur et les blackbones
        :return: une représentation structurée de la solution
        :rtype: Solution
        """
        a = Algo(self)

        a = a.solve()
        

        return 0
